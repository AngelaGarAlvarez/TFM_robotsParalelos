'''
Created on 2020

@author: Angela Garcia Alvarez
'''
import numpy as np
from problem import Problem
from src.robots.fivebar.fivebar import Fivebar
from src.robots.utils.validPoint import ValidPoint
import random as rnd

class FivebarProblem(Problem):

    def __init__(self, obj):
        '''
        Constructor
        :param obj: dimensions of the objective region
        '''
        Problem.__init__(self, obj, name="Fivebar", dim=3)
        self.l, self.L = obj

    def uniform(self):
        '''
        Random values for each parameter
        :return: list with genome values
        '''
        l = round(rnd.uniform(1, self.max),2)
        L = round(rnd.uniform(1, l),2)
        d = round(rnd.uniform(1,  l+L),2)
        return [l, L, d]

    def setRobot(self, indiv):
        '''
        Set Fivebar robot
        :param indiv: params to define the manipulator
        '''
        self.robot = Fivebar(indiv[0], indiv[1], indiv[2], self.nTot)

    def MaxWorkspace(self):
        '''
        Get area of the maximum workspace
        :return: volumne
        '''
        return (self.max*2) * ((self.max*2) *2)

    def _rectInsid(self,l,L):
        '''
        Check if rectangle is inside workspace
        :param l: smallest dimension of the objective region
        :param L: largest dimension of the objective region
        :return: points and if is inside or not
        '''
        X = self.robot.center.x - (l / 2.)
        X2 = self.robot.center.x + (l / 2.)
        Y = self.robot.center.y - (L / 2.)
        Y2 = self.robot.center.y + (L / 2.)
        Y3 = self.robot.center.y + (L / 4.)
        points = [ValidPoint(x, y) for x in (X, X2, 0)
                  for y in (Y, Y2, Y3)]
        return points, any([not p for p in points])

    def spaceInside(self):
        '''
        check if objective region is inside workspace
        :return: points that are inside workspace
        '''
        points, valid = self._rectInsid(self.l, self.L)
        if not valid:
            points, valid = self._rectInsid(self.L, self.l)
        return points