'''
Created on 2020

@author: Angela Garcia Alvarez
'''
from src.optimization.problems.fivebarProblem import FivebarProblem
from src.optimization.problems.deltaProblem import DeltaProblem
from src.optimization.moeas.spea2 import SPEA2
from src.optimization.moeas.nsga2 import NSGAII
from src.optimization.moeas.nsga3 import NSGAIII
import pathos.multiprocessing as mp
import os.path
import numpy as np
import utils.csvUtils as csvAux
import utils.experimentUtils as aux
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

def testMOEA(ga):
    '''
    Evolve MOEA
    :param ga: moea to evolve
    :return: population and last logbook
    '''
    pop, logbook = ga.evolve()
    return pop, logbook[-1]

def bestIndv(pop):
    '''
    Get the "best" individual as the best f1 individual
    :param pop: population
    :return: "best" individual
    '''
    indvList = [aux.Indv(i, i.fitness.values) for i in pop]
    indvList.sort(key=lambda x: x.f1, reverse=True)
    print [i.f1 for i in indvList]
    return indvList[0]

def saveResults(experiment, pops):
    '''
    Save results in csv and LaTeX files
    :param experiment: experiment information
    :param pops: population
    '''
    indvList = [bestIndv(pop) for pop in pops]
    medList = [np.around(np.array(b.f, dtype=np.float64), decimals=4) for b in indvList]
    csvAux.saveResults(experiment, indvList, medList, fileCSV, fileLatex, fileExperiment)

def test(Ntest, experiment):
    '''
    Test MOEAs Ntest times
    :param Ntest: number of tests
    :param experiment: experiment information
    '''
    print experiment.moea, experiment.prob.name, experiment.info
    prob, N, g, c, m = experiment.getParams()
    switcher = {
        "SPEA2": [SPEA2(prob, N, g, c, m)],
        "NSGAII": [NSGAII(prob, N, g, c, m)],
        "NSGAIII": [NSGAIII(prob, N, g, c, m)],
    }
    gas = switcher.get(experiment.moea, [SPEA2(prob, N, g, c, m)]) * Ntest
    pool = mp.Pool(Ntest)
    pops, looks = zip(*pool.map(testMOEA, gas))
    pool.close()
    saveResults(experiment, pops)

def preprocessAndTest(path, Ntest, experiment):
    '''
    Preprocess files, test and save results
    :param path: A path to the files
    :param Ntest: Number of individual executions
    :param experiment: experiment info
    :return:
    '''
    global fileCSV, fileLatex, fileExperiment
    resultPath = "../results/" + experiment.moea + "/"
    if not os.path.exists(os.path.join(path,resultPath )):
        os.makedirs(os.path.join(path, resultPath))
    fileName = experiment.moea + experiment.prob.name + "Summary"
    fileExperimentName = experiment.moea + experiment.prob.name + experiment.file
    fileCSVname = os.path.join(path, resultPath + fileName+ ".csv")
    fileLatexName = os.path.join(path, resultPath + "LATEX_" + fileName+ ".txt")
    fileExperimentName = os.path.join(path, resultPath + fileExperimentName+ ".csv")
    try:
        fileExperiment = open(fileExperimentName)
        fileExperiment.close()
    except IOError:
        fileExperiment = open(fileExperimentName, "a")
        fileCSV = open(fileCSVname, "a")
        fileLatex = open(fileLatexName, "a")
        test(Ntest, experiment)
        fileCSV.close()
        fileLatex.close()
        fileExperiment.close()
#
def testAll(Ntest=30, gens=[100, 200, 300], pops=[[52,13], [100,25], [200,50]], cros=[.9, .8, .6], mut=[.1, 1. / 4, 1. / 3],
            fiveParams = (100,100), deltaParams = (100, 100, 100)):
    '''
    Tets all the parametrizations, robots and MOEs
    :param Ntest: number of independent experiments
    :param gens: list of number of generatios
    :param pops: list of size of populations (and H)
    :param cros: list o f crossover values
    :param mut: list of mutation values
    :param fiveParams: parameters for Fivebar problem
    :param deltaParams: parameters for Delta problem
    '''
    moeas = ["SPEA2","NSGAII", "NSGAIII"]
    my_path = os.path.abspath(os.path.dirname(__file__))
    probs = [FivebarProblem(fiveParams), DeltaProblem(deltaParams)]
    experiments = [aux.Experiment(c, m, g, N, moea, prob) for N in pops for g in gens for m in mut for c in cros
                   if N[0] < g for prob in probs for moea in moeas]
    [experiments[e-1].setName("E%d"%(e)) for e in range(1, len(experiments)+1)]
    [preprocessAndTest(my_path, Ntest, experiment) for experiment in experiments]

if __name__ == '__main__':
    testAll()
