'''
Created on 2020

@author: Angela Garcia Alvarez
'''
from src.optimization.moeas.moea import MOEA
from deap import tools
import matplotlib.pyplot as plt
import numpy
from deap import algorithms
import random as rnd
import math

class NSGAIII(MOEA):

    def __init__(self, problem, H, gen, crossover, mutation):
        '''
        Constructor of NSGA-III
        :param problem: problem to resolve
        :param size: size of the populations
        :param gen: number of generations
        :param crossover: % for the crossover
        :param mutation: % for the mutation
        '''
        MOEA.__init__(self, problem, H, gen, crossover, mutation)
        NOBJ = 3
        P = H - (NOBJ-1)
        self.size = int(H + (4 - H % 4))
        # Create, combine and removed duplicates
        ref_points = tools.uniform_reference_points(NOBJ, P)
        self.tb.register("select", tools.selNSGA3, ref_points=ref_points)

    def _initPop(self):
        '''
        Init population
        :return:
        '''
        pop = self.tb.population(n=self.size)
        # Evaluate the individuals with an invalid fitness
        invalid_ind = self.evaluateInvalid(pop)
        # This is just to assign the crowding distance to the individuals
        # no actual selection is done
        return pop, invalid_ind


    def _getOffspring(self, pop):
        '''
        Get offspring of a population
        :param pop: population
        :return: list with the offspring
        '''
        offspring = algorithms.varAnd(pop, self.tb, self.cx, self.mt)
        return [self.tb.clone(ind) for ind in offspring]

    def _getPop(self, pop):
        '''
        Get population
        :param pop: original population
        :return: population and invalid individuals
        '''
        offspring = algorithms.varAnd(pop, self.tb, self.cx, self.mt)
        # Evaluate the individuals with an invalid fitness
        invalid_ind = self.evaluateInvalid(offspring)
        # Select the next generation population from parents and offspring
        pop = self.tb.select(pop + offspring, self.size)
        return pop, invalid_ind
