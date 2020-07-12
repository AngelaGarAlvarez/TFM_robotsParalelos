'''
Created on 2020

@author: Angela Garcia Alvarez
'''
from math import sin, cos
import numpy as np
from src.robots.utils.validPoint import ValidPoint

class PointF(ValidPoint):

    def __init__(self, x, y, qs, L):
        '''
        Constructor
        :param x: coordinate in x axis
        :param y: coordinate in y axis
        :param qs: angles fo the manipulator to get the point
        :param L: linkage of the robot needed for the jacobin calculation
        '''
        ValidPoint.__init__(self, x, y, None, qs)
        self.jacobian(L)
        self.conditionIndex()
        self.stiffness()

    def jacobian(self, L):
        '''
        Calcualtes Jacobian fo the point
        :param L: link of the manipulator
        :return: Jacobian matrix of he point
        '''
        qs = self.qs
        self.J =  L/ sin(qs[3] - qs[2]) * np.array([[sin(qs[3]) * sin(qs[0] - qs[2]),
                                                     -sin(qs[2]) * sin(qs[1] - qs[3])],
                                                    [-cos(qs[3]) * sin(qs[0] - qs[2]),
                                                     cos(qs[2]) * sin(qs[1] - qs[3])]])