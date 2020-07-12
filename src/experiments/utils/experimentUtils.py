'''
Created on 2020

@author: Angela Garcia Alvarez
'''

class Indv:
    def __init__(self, K, fs):
        '''
        Constructor of an object with basic deinition of an individual(desing) of a manipulator
        :param K: parameters for the manipulator
        :param fs: fitness values
        '''
        self.K = K
        self.f = fs
        self.f1 = fs[0]
        self.f2 = fs[1]
        self.f3 = fs[2]

class Experiment:
    def __init__(self, c, m, g, N, moea, prob, name=None):
        '''
        Constructor of basic class to define Experiment
        :param c: crossover
        :param m: mutation
        :param g: generations
        :param N: size of population or H for NSGA-III
        :param moea: name of the MOEA
        :param prob: problem definition
        :param name: name of the experiment
        '''
        self.name = name
        self.c, self.m, self.g= c, m, g
        self.moea = moea
        self.prob = prob
        letters = ["pop", "H"]
        i = self._getIndex(moea)
        self.N = N[i]
        self.info = "[P_{c}=%.2f, P_{m}= %.2f, P_{g}=%d, P_{%s}=%d] ; " % (c, m, g, letters[i], self.N)
        self.file = "-Cross%.2f-mut%.2f-gens%d" % (c, m, g)

    def setName(self, name):
        '''
        Set name of the experiment
        :param name:
        :return:
        '''
        self.name=name

    def _getIndex(self, moea):
        '''
        Get index for N (H for NSGA-III, size for the rest)
        :param moea: name of the MOEA
        :return: index to get N
        '''
        if (moea == "NSGAIII"):
            return 1
        return 0

    def getParams(self):
        '''
        Return params of the experiment
        '''
        return self.prob, self.N, self.g, self.c, self.m