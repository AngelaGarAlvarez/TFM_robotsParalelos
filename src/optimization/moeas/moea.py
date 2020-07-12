'''
Created on 2020

@author: Angela Garcia Alvarez
'''
import numpy as np
import random as rnd
import array as arr
from deap import base
from deap import tools
from deap import creator

creator.create("Fitness", base.Fitness, weights=(1, 1.0, 1.0))
creator.create("Individual", arr.array, typecode='d', fitness=creator.Fitness)

class MOEA(object):

    def __init__(self, problem, size, gen, crossover, mutation):
        '''
        Constructor
        :param problem: problem to resolve
        :param size: size of the populations
        :param gen: number of generations
        :param crossover: % for the crossover
        :param mutation: % for the mutation
        '''
        self.problem = problem
        self.size = size
        self.gen = gen
        self.cx = crossover
        self.mt = mutation
        self.tb = base.Toolbox()
        self.tb = base.Toolbox()
        self.tb.register("attr_double", self.problem.uniform)

        self.tb.register("individual", tools.initIterate, creator.Individual, self.tb.attr_double)
        self.tb.register("population", tools.initRepeat, list, self.tb.individual)

        self.tb.register("evaluate", self.problem.getFitness)
        bound_low, bound_up = self.problem.getBounds()

        self.tb.register("mate", tools.cxSimulatedBinaryBounded, low=bound_low, up=bound_up,
                         eta=30.0)
        self.tb.register("mutate", tools.mutPolynomialBounded, low=bound_low, up=bound_up, eta=20.0,
                         indpb=1.0 / self.problem.dim)

        self.header = ["median", "gen"]


    def evaluateInvalid(self, offspring):
        '''
        Evaluate ivalid individuals based in it fitness
        :param offspring: list of individuals
        :return: list of individuals evaluated
        '''
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = self.tb.map(self.tb.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        return invalid_ind

    def evolution(self, pop, gen, stats, logbook):
        '''
        Evolution of a generation
        :param pop: population
        :param gen: generations
        :param stats: stats to complete
        :param logbook: log to save stats and results
        :return:
        '''
        # Vary the population
        pop, invalid_ind = self._getPop(pop)
        record = stats.compile(pop)
        logbook.record(gen=gen, **record)
        print(logbook.stream)

    def evolve(self, seed=None):
        '''
        Evolution process
        :param seed:
        :return:
        '''
        rnd.seed(seed)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("median", np.nanmean, axis=0)
        logbook = tools.Logbook()
        logbook.header = self.header
        pop, invalid_ind = self._initPop()
        record = stats.compile(pop)
        logbook.record(gen=0, **record)
        print(logbook.stream)
        # Begin the generational process
        [self.evolution(pop, gen, stats, logbook) for gen in range(1, self.gen)]

        return pop, logbook