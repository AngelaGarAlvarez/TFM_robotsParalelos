'''
Created on 2020

@author: Angela Garcia Alvarez
'''
import numpy as np

class Robot:

    def __init__(self, l, L, nTot=1000):
        '''
        Constructor
        :param l: one linkage of the robot
        :param L: one likage of the robot
        :param nTot: number of points for the workspace calculation
        '''
        self.L = L
        self.l = l
        self.center = None
        self.w = None
        self.wt = None
        self.nTot = nTot
        self.CGI = None
        self.RGI = None

    def getGlobalCondition(self):
        '''
        Calculate global condition Index of the robot
        :return: Global Condition Index as float
        '''
        if type(self.RGI) == type(None):
            w = self.getWorkspace()
            C = np.sum([p.ci for p in w])
            self.RGI = C / len(w)
        return self.RGI

    def getStiffness(self):
        '''
        Calculte Global Stiffness Index of the robot
        :return: Global Stiffness Index as float
        '''
        if type(self.CGI) == type(None):
            w = self.getWorkspace()
            S = np.sum([p.s for p in w])
            self.CGI = S / len(w)
        return self.CGI

    def _pointsIn(self, points):
        '''
        Select point that are inside workspace
        :param points: A list of points that may be in workspace
        :return: list of points that are inside workspace
        '''
        pointsIn = [self.pointIn(p) for p in points]
        return [p for p in pointsIn if p]

    def getWorkspace(self):
        '''
        Calculate aproximation of workspace based in Montcarlo method
        :return:
        '''
        if type(self.w) == type(None):
            pTot = self._delimiter() #Obtain delimter space for the manipulator type
            pIn = self._pointsIn(pTot) #Select points that are inside workspace
            self.w = np.array(pIn)
        return self.w

    # def calculateAll(self):
    #     '''
    #     Calculate all the
    #     :return:
    #     '''
    #     self.getWorkspaceDim()
    #     self.getStiffness()
    #     self.getGlobalCondition()
    #     self.w = None