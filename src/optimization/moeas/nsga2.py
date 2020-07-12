'''
Created on 2020

@author: Angela Garcia Alvarez
'''
from src.optimization.moeas.moea import MOEA
from deap import tools
import random as rnd

class NSGAII(MOEA):

    def __init__(self, problem, size, gen, crossover, mutation):
        '''
        Constructor of NSGA-II
        :param problem: problem to resolve
        :param size: size of the populations
        :param gen: number of generations
        :param crossover: % for the crossover
        :param mutation: % for the mutation
        '''
        MOEA.__init__(self, problem, size, gen, crossover, mutation)
        self.tb.register("select", tools.selNSGA2)

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
        return self.tb.select(pop, len(pop)), invalid_ind

    def _getOffspring(self, pop):
        '''
        Get offspring of a population
        :param pop: population
        :return: list with the offspring
        '''
        offspring = tools.selTournamentDCD(pop, len(pop))
        return [self.tb.clone(ind) for ind in offspring]

    def _getPop(self, pop):
        '''
        Get population
        :param pop: original population
        :return: population and invalid individuals
        '''
        # Vary the population
        offspring = self._getOffspring(pop)

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if rnd.random() <= self.cx:
                self.tb.mate(ind1, ind2)

            if rnd.random() <= self.mt:
                self.tb.mutate(ind1)
            if rnd.random() <= self.mt:
                self.tb.mutate(ind2)

            del ind1.fitness.values, ind2.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = self.evaluateInvalid(offspring)

        # Select the next generation population
        pop = self.tb.select(pop + offspring, self.size)
        return pop, invalid_ind

