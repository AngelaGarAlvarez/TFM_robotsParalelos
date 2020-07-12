'''
Created on 2020

@author: Angela Garcia Alvarez
'''
import numpy as np
from src.robots.utils.validPoint import ValidPoint

class PointD(ValidPoint):

    def __init__(self, x, y, z, qs, l, ths):
        '''
        Constructor
        :param x: coordinate in x axis
        :param y: coordinate in y axis
        :param z: coordinate in z axis
        :param qs: angles fo the manipulator to get the point
        :param L: linkage of the robot needed for the jacobin calculation
        :param ths: angles of the robot
        '''
        ValidPoint.__init__(self, x, y, z, qs)
        self.jacobian(l, ths)
        self.conditionIndex()
        self.stiffness()

    def jacobian(self, l, ths):
        '''
        Calcualtes Jacobian fo the point
        :param L: link of the manipulator
        :param ths: angles of the robot
        :return: Jacobian matrix of he point
        '''
        q1s = self.qs[0]
        q2s = self.qs[1]
        q3s = self.qs[2]

        jF1s = np.cos(q2s) * np.sin(q3s) * np.cos(ths) - np.cos(q3s) * np.sin(ths)
        jF2s = np.cos(q3s) * np.cos(ths) + np.cos(q2s) * np.sin(q3s) * np.sin(ths)
        jF3s = np.sin(q2s) * np.sin(q3s)

        JI = np.identity(3) * (l + np.sin(q2s - q1s) * np.sin(q3s))
        JF = [jF1s, jF2s, jF3s]

        self.J = np.dot(np.linalg.inv(JI), JF)