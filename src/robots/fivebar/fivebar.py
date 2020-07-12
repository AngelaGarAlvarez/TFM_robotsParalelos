'''
Created on 2020

@author: Angela Garcia Alvarez
'''
from math import sin, cos, atan2, sqrt
import random as rnd
from src.robots.utils.point import Point
from pointFivebar import PointF
from src.robots.robot import Robot
import numpy as np
class Fivebar (Robot):

    def __init__(self, l, L, d, nTot=1000):
        '''
        Constructor
        :param l: largest linkage of the fivebar
        :param L: smallest likage of the fivebar
        :param nTot: number of points for the workspace calculation
        '''
        Robot.__init__(self, l, L, nTot)
        self.d = d

    def _getAngles(self, sigmas, aux, xp, yp):
        '''
        Calculate the position angles of the manipulator to get to the point
        :param sigmas: sigmas of the manipulator's composition
        :param aux: auxiliary vectors for the inverse cinematic calculation
        :param xp: position in x axis
        :param yp: position in y axis
        :return: list of angles to get effector position (empty if point is outside workspace)
        '''
        sign = lambda a: (a > 0) ^ (a < 0)
        L = self.L
        l = self.l
        sq = aux["B"]**2 - (aux["C"]**2 - aux["A"]**2)
        if sq <0:
            return []
        q1 = 2*atan2(-aux["B"] + sigmas[0] * sqrt(sq), aux["C"] - aux["A"])
        sq = aux["B"] ** 2 - (aux["F"] ** 2 - aux["E"] ** 2)
        if sq <0:
            return []
        q2 = 2 * atan2(-aux["B"] + sigmas[1] * sqrt(sq), aux["F"] - aux["E"])
        sq = aux["b"] ** 2 - (aux["f"]**2 - aux["e"] ** 2)
        if sq <0:
            return []
        sign = sign(yp)*sign(yp - l*sin(q1))
        q3 = 2 * atan2(-aux["b"] + sign*sqrt(sq), aux["f"] - aux["e"])

        landa = l*cos(q2) - l*cos(q1) + self.d
        mi = l*sin(q2)- l*sin(q1)
        M = 2*L*landa
        N = 2*L*mi
        P = - landa**2 - mi**2
        sq = M ** 2 + N ** 2 - P ** 2
        if sq < 0:
            return []
        q4 = atan2(sqrt(sq), P) + atan2(N ** 2, M ** 2)
        return [q1, q2, q3, q4]

    def _getAux(self, point):
        '''
        Calculate auxiliary constants needed for inverse cinematic calculation
        :param point: point for which they are calculated
        :return: dictionary auxiliary constants for angles calculation
        '''
        L = self.L
        l = self.l
        D = self.d / 2.
        xp = point.x
        yp = point.y
        aux ={"A": -(2 * l) * (xp - D),
              "B": -2 * yp * l,
              "b": -2 * yp * L,
              "C": (xp - D) ** 2 + yp ** 2 + l ** 2 - L ** 2,
              "E": -(2 * l) * (xp + D),
              "e": -(2 * L) * (xp + D),
              "F": (xp + D) ** 2 + yp ** 2 + l ** 2 - L ** 2,
              "f": (xp + D) ** 2 + yp ** 2 - l ** 2 + L ** 2}
        return aux

    def inverseKinematics(self, point):
        '''
        Calculate inverse kinematics of a point
        :param point: point for which it is calculated
        :return: list of angles of the point, empty if it is outside workspace
        '''
        aux = self._getAux(point)
        qs = [self._getAngles([sigma1, sigma2], aux, point.x, point.y) for sigma1 in [-1,1] for sigma2 in [-1, 1]]
        return [q for q in qs if len(q) > 0]

    def _delimiter(self):
        '''
        Calculates the maximum hypothetical workspace for Monte Carlo method
        :return:list woth of  random points in the maximum hypothetical workspace
        '''
        pTot = []
        sq = (self.l + self.L)**2 -(self.d/2.0) **2
        if sq < 0:
            return pTot
        maxX = self.L + self.l - self.d / 2.
        minY, minX, maxY = 0, -maxX, sqrt(sq)
        self.center = Point(0, maxY/2.0)
        #generates random points in the hypothetical workspace
        for n in range(0, self.nTot):
            x = rnd.uniform(minX, maxX)
            y = rnd.uniform(minY, maxY)
            pTot = np.append(pTot, Point(x, y))

        return pTot

    def pointIn(self, p):
        '''
        Obtain a point with specific cinematic values for a point if it is inside workspace
        :param p: point to check
        :return: list of points with stiffness and condition calculated for the original point coordinates, empty if point it is outside
        '''
        points = [PointF(p.x, p.y, qs, self.L) for qs in self.inverseKinematics(p) if len(qs)>0]
        if len(points) == 0:
            return []
        return rnd.choice(points)

    def getWorkspaceDim(self):
        '''
        Calculate area of the worinvkspace
        :return: area of the workspace
        '''
        if self.wt is None:
            self.wt = 0
            if len(self.getWorkspace()) > 0:
                y = sqrt((self.l + self.L)**2 -(self.d/2.0) **2)
                x = 2 * (self.L + self.l - self.d / 2)
                self.wt = y * x * (len(self.getWorkspace()) / float(self.nTot))
        return self.wt