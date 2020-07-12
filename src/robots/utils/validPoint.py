'''
Created on 2020

@author: Angela Garcia Alvarez
'''
import numpy as np
from src.robots.utils.point import Point


class ValidPoint(Point):

    def __init__(self, x, y, z=None, qs=None):
        '''
        Constructor
        :param x: coordinate in x axis
        :param y: coordinate in y axis
        :param z: coordinate in z axis
        :param qs: angles fo the manipulator to get the point
        '''
        Point.__init__(self, x, y, z)
        self.qs = qs
        self.J = None
        self.ci = None
        self.s = None

    def conditionIndex(self):
        '''
        Calculate condition index
        :return: condition index of the point
        '''
        c = np.linalg.cond(self.J)
        self.ci = 1 / c

    def stiffness(self):
        '''
        Calculate stiffness index
        :return: stiffness index of the point
        '''
        K = np.dot(np.transpose(self.J), self.J)
        s = np.linalg.cond(K)
        self.s = 1 / s

