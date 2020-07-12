'''
Created on 2020

@author: Angela Garcia Alvarez
'''
import numpy as np
from problem import Problem
from src.robots.delta.delta import Delta
import random as rnd
from math import pi
from src.robots.utils.validPoint import ValidPoint
import itertools

class DeltaProblem(Problem):

    def __init__(self, obj):
        '''
        Constructor
        :param obj: dimensions of the objective region
        '''
        Problem.__init__(self, obj, name="Delta", dim=4)
        self.num = 0
        self.a, self.g, self.h = obj

    def getBounds(self):
        '''
        Calculates bounds to manipulator parameter
        :return: list of bounds
        '''
        return ([1] * self.dim, [self.max, self.max, self.max/2., self.max/2.])

    def uniform(self):
        '''
        Random values for each parameter
        :return: list with genome values
        '''
        L = round(rnd.uniform(1, self.max),2)
        l = round(rnd.uniform(1, L),2)
        b = round(rnd.uniform(1, l),2)
        p = round(rnd.uniform(1, b),2)
        return [l, L, b, p]

    def setRobot(self, indiv):
        '''
        Set Delta robot
        :param indiv: params to define the manipulator
        '''
        self.robot = Delta(indiv[0], indiv[1], indiv[2], indiv[3], self.nTot)

    def MaxWorkspace(self):
        '''
        Get volume of the maximum workspace
        :return: volumne
        '''
        return 2/3. *  pi *  (self.max ** 3)

    def human_readable_extra(self):
        return "\n\tDelta problem"

    def _cubeInside(self, (a, g, h)):
        '''
        Check if prisma is inside workspace
	    :param a: width of the objective region
	    :param g: depth of the objective region
	    :param h: height of the objectve region
        :return: points and if is inside or not
        '''
        X = self.robot.center.x - (a /2.)
        X1 = self.robot.center.x + (a /2.)
        Y = self.robot.center.y - (g /2.)
        Y1 = self.robot.center.y + (g /2.)
        Z = self.robot.center.z - (h /2.)
        Z1 = self.robot.center.z + (h /2.)
        points = [ValidPoint(x, y, z) for x in (X, X1) for y in (Y, Y1) for z in (Z,Z1)]
        return points, any([not p for p in points])

    def spaceInside(self):
        '''
        check if objective region is inside workspace
        :return: points that are inside workspace
        '''
        valid = False
        i = 0
        comb = list(itertools.permutations([self.a,self.g,self.h]))
        while not valid and i<len(comb):
            points, valid = self._cubeInside(comb[i])
            i +=1
        return points