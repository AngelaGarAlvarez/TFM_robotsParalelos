'''
Created on 2020

@author: Angela Garcia Alvarez
'''

import numpy as np
import random as rnd

class Problem(object):

    def __init__(self, obj, name=None, dim=3):
        '''
        Constructor
        :param obj: dimensions of the objective region
        :param name: name of the manipulator
        :param dim: dimensions of the problem parameters
        '''
        self.dim = dim
        self.robot = None
        self.name = name
        self.obj = obj
        self._setNTot()
        self.wo = np.prod(obj)
        self.max = np.sum(self.obj)

    def _setNTot(self):
        '''
        Set the number of points or the workspace calculation(Monte Carlo method)

        '''
        count = 1
        div = np.prod(self.obj)/(len(self.obj)*10)
        while div > 10:
            div = div / 10
            count += 1
        nTot = 10 ** count
        self.nTot = nTot if nTot<10000 else 10000
        self.nTot = 1000

    def getBounds(self):
        '''
        Calculates bounds to manipulator parameter
        :return: list of bounds
        '''
        return([1]*self.dim,[self.max]*self.dim)

    def getF1(self):
        '''
        Calculates F1 (one of the functions to optimize)
        :return: value for F1
        '''
        return (self.robot.getWorkspaceDim() - self.wo) / float(self.MaxWorkspace() - self.wo)

    def getNu(self):
        '''
        Calculates Nu to complete F1
        :return: Nu value
        '''
        points = self.spaceInside()
        pins = [self.robot.pointIn(p) for p in points]
        self.robot.pointIn(points[0])
        pins = [p for p in pins if p]
        nu = len(pins) - len(points)
        nu = nu*self.wo if nu < 0 else 1
        return nu

    def getFitness(self, K):
        '''
        Calculates fitness values (three functions)
        :param K: list of parameters to define manipulator
        :return: list of function values
        '''
        self.setRobot(K)
        if self.robot.getWorkspaceDim() == 0:
               return [-(2**len(self.obj))*self.wo, -self.wo, -self.wo]
        f1 = self.getF1()
        nu = self.getNu()
        v = -1 if nu < 0 else 1
        z = -1 if self.robot.getWorkspaceDim() < self.wo or nu == 1 else 1

        f1 = nu*z*f1
        f2 = v*self.robot.getStiffness()
        f3 = v*self.robot.getGlobalCondition()
        return [f1, f2, f3]

    def uniform(self):
        '''
        Random values for the parameters
        :return:
        '''
        return [round(rnd.uniform(a, b),2) for a, b in zip(*self.problem.getBounds())]