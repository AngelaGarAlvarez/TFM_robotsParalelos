import numpy as np
import pathos.multiprocessing as mp
import time

class Robot:

    def __init__(self, l, L, nTot=1000):
        self.L = L
        self.l = l
        self.center = None
        self.w = None
        self.wt = None
        self.nTot = nTot
        self.CGI = None
        self.RGI = None

    def getGlobalCondition(self):
        if type(self.RGI) == type(None):
            w = self.getWorkspace()
            C = np.sum([p.ci for p in w])
            self.RGI = C / len(w)
        return self.RGI

    def getStiffness(self):
        if type(self.CGI) == type(None):
            w = self.getWorkspace()
            S = np.sum([p.s for p in w])
            self.CGI = S / len(w)
        return self.CGI

    def _pointsIn(self, points):
        pointsIn = [self.pointIn(p) for p in points]
        return [p for p in pointsIn if p]

    def getWorkspace(self):
        if type(self.w) == type(None):
            pTot = self._delimiter()
            pIn = self._pointsIn(pTot)
            self.w = np.array(pIn)
        return self.w

    def calculateAll(self):
        self.getWorkspaceDim()
        self.getStiffness()
        self.getGlobalCondition()
        self.w = None