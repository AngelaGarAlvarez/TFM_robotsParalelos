'''
Created on 2020

@author: Angela Garcia Alvarez
'''
from src.optimization.moeas.moea import MOEA
from deap import tools, algorithms
import random as rnd

class SPEA2(MOEA):

    def __init__(self, problem, size, gen, crossover, mutation):
        '''
        Constructor of SPEA2
        :param problem: problem to resolve
        :param size: size of the populations
        :param gen: number of generations
        :param crossover: % for the crossover
        :param mutation: % for the mutation
        '''
        MOEA.__init__(self, problem, size, gen, crossover, mutation)
        self.tb.register("select", tools.selSPEA2)

    def _initPop(self):
        pop = self.tb.population(n=self.size)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = self.evaluateInvalid(pop)

        # This is just to assign the crowding distance to the individuals
        # no actual selection is done
        return pop, invalid_ind

    def _getOffspring(self, pop):
        offspring = algorithms.varAnd(pop, self.tb, self.cx, self.mt)
        return [self.tb.clone(ind) for ind in offspring]

    def _getPop(self, pop):
        offspring = algorithms.varAnd(pop, self.tb, self.cx, self.mt)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = self.evaluateInvalid(offspring)

        # Select the next generation population from parents and offspring
        pop = self.tb.select(pop + offspring, self.size)
        return pop, invalid_ind