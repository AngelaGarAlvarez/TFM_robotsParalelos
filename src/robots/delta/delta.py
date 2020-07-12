'''
Created on 2020

@author: Angela Garcia Alvarez
'''
from math import sqrt, pi, radians, sin, cos
import numpy as np
import random as rnd
from src.robots.utils.point import Point
from pointDelta import PointD
from src.robots.robot import Robot

class Delta (Robot):

    def __init__(self, l, L, b, p, nTot=10000):
        '''
        Constructor
        :param l: smallest linkage of the fivebar
        :param L: largest linkage of the fivebar
        :param b: distane brom center to linkages in the base
        :param p: distane brom center to linkages in the efector
        :param nTot: number of points for the workspace calculation
        '''
        Robot.__init__(self, l, L, nTot)
        # cambiar lo de las r  y s
        # rb = radio circulo inscrito en base
        self.b = b
        self.rb = b * sqrt(3) / 6
        # rp = radio circulo circunscrito en plataforma final
        self.p = p
        self.rp = p * sqrt(3) / 3

        self.ths = np.array([0, 2 * pi / 3.0, 4 * pi / 3.0], dtype=np.double)

    def _vectorsA(self, point):
        '''
        Calculate auxiliary vectors needed for inverse cinematic calculation
        :param point: point for which they are calculated
        :return: three arrays of auxiliary vectors
        '''
        aus = np.cos(self.ths, dtype=np.double) * point.x + np.sin(self.ths, dtype=np.double) * point.y - self.rp
        avs = - np.sin(self.ths, dtype=np.double) * point.x + np.cos(self.ths, dtype=np.double) * point.y
        aws = point.z * np.ones(3)
        return aus, avs, aws

    def _vectorsS(self, aus, aws, q3s):
        '''
        Calculate auxiliary vectors needed for inverse cinematic calculation based in other vectors
        :param aus: vector base for the calculating
        :param aws: vector base for the calculating
        :param q3s: angle base for the calculating
        :return: three arrays with auxiliary vector
        '''

        s0s = aws ** 2 + aus ** 2 + 2 * self.rb * aus - 2 * self.l * aus + \
              self.l ** 2 + self.rb ** 2
        s1s = -4 * self.l * aws ** 2
        s2s = aws ** 2 + aus ** 2 + 2 * self.rb * aus + 2 * self.l * aus + \
              self.l ** 2 + self.rb ** 2 - self.L ** 2 * np.sin(q3s) ** 2 + \
              2 * self.l * self.rb
        return s0s, s1s, s2s

    def _angles(self, s0s, s1s, s2s, aus, q3s):
        '''
        Calculate the position angles of the manipulator to get to the point

        :param s0s: auxiliary vectors for the inverse cinematic calculation
        :param s1s: auxiliary vectors for the inverse cinematic calculation
        :param s2s: auxiliary vectors for the inverse cinematic calculation
        :param aus: auxiliary vectors for the inverse cinematic calculation
        :param q3s: auxiliary angles for the inverse cinematic calculation
        :param yp: position in y axis
        :return: list of angles to get effector position (empty if point is outside workspace)
        '''

        qsP, qsN = [], []
        sqs = s1s ** 2 - 4 * s2s * s0s
        if any(sq <0 for sq in sqs):
            return [],[]

        t1sp = (-s1s + np.sqrt(sqs, dtype=np.double)) / (2 * s2s)
        t1sn = (-s1s - np.sqrt(sqs, dtype=np.double)) / (2 * s2s)

        q1sP = 2 * np.arctan(t1sp, dtype=np.double)
        q1sN = 2 * np.arctan(t1sn, dtype=np.double)

        div = self.L * np.sin(q3s)
        if all(d>0 for d in div):
            inside = (np.subtract(aus, self.l * np.cos(q1sP)) + self.rb) / div
            if all(-1<= i <= 1 for i in inside):
                qsP = [q1sP, np.arccos(inside, dtype=np.double), q3s]
            inside = (np.subtract(aus, self.l * np.cos(q1sN) + self.rb)) / div
            if all(-1<= i <= 1 for i in inside):
                qsN = [q1sN, np.arccos(inside, dtype=np.double), q3s]

        return qsP + qsN

    def _getAngles(self, aus, avs, aws, sign):
        '''
        Calculate the position angles of the manipulator to get to the point by the efector
        :param aus: auxiliary vectors for the inverse cinematic calculation
        :param avs: auxiliary vectors for the inverse cinematic calculation
        :param aws: auxiliary vectors for the inverse cinematic calculation
        :param sign: sign of the manipulator composition
        :return: list of angles to get effector position (empty if point is outside workspace)
        '''

        angles = []
        inside = avs / self.L
        if all(-1<= i <= 1 for i in inside):
            q3s = sign * np.arccos(inside)
            s0s, s1s, s2s = self._vectorsS(aus, aws, q3s)
            qs = self._angles(s0s, s1s, s2s, aus, q3s)
            angles = [q for q in qs if len(q)>0]
        return angles

    def inverseKinematics(self, point):
        '''
        Calculate inverse kinematics of a point
        :param point: point for which it is calculated
        :return: list of angles of the point, empty if it is outside workspace
        '''
        aus, avs, aws = self._vectorsA(point)
        if np.any(avs/self.L > 1):
            return []
        qs = [self._getAngles(aus, avs, aws, sign) for sign in [-1, 1]]
        return [q for q in qs if len(q)>0]

    def _generatePoint(self):
        '''
        Generate random point inside hypothetical maximum workspace
        :return: random Point inside
        '''
        R = self.L + self.l + self.p + self.b
        th = radians(rnd.uniform(0, 90))
        ah = radians(rnd.uniform(0, 360))
        r = rnd.uniform(0, R)

        x = r * sin(th) * cos(ah)
        y = r * sin(th) * sin(ah)
        z = - r * cos(th)
        return Point(x, y, z)

    def inHemis(self, p):
        '''
        Check if it is in the hemisphere
        :param p: point to check
        :return: True if point is inside hemisphere
        '''
        r = self.L + self.l + self.p + self.b
        if (p.x ) ** 2 + (p.y ) ** 2 + (p.z) ** 2 < r ** 2:
            if p.z < 0:
                return True
        return False

    def pointIn(self, p):
        '''
        Check if point is inside workspace
        :param p: point to check
        :return: Delta points with stiffness and condition index inside workspace
        '''
        if not self.inHemis(p):
            return []
        points = [PointD(p.x, p.y, p.z, qs, self.l, self.ths) for qs in self.inverseKinematics(p) if len(qs)>0]
        if len(points) == 0:
            return []
        return rnd.choice(points)

    def _delimiter(self):
        '''
        Calculates the maximum hypothetical workspace for Monte Carlo method
        :return: random points in the maximum hypothetical workspace
        '''
        R = self.L + self.l + self.p + self.b
        self.center = Point(0, 0, -R*.5)
        return [self._generatePoint() for n in range(0, self.nTot)]

    def getWorkspaceDim(self):
        '''
        Calculate volume of the workspace
        :return: volume of the workspace
        '''
        if self.wt is None:
            self.wt = 0
            if len(self.getWorkspace()) > 0:
                self.wt = 2/3. * ( pi * ((self.L + self.l + self.rb + self.rp) ** 3)) * (len(self.getWorkspace())
                                                                                         / float(self.nTot))
        return self.wt