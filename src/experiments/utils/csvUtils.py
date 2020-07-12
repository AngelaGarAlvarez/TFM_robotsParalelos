'''
Created on 2020

@author: Angela Garcia Alvarez
'''

import numpy as np

def format_numbers(numbers):
    '''
    Formt numbers in scientific format to save in LaTeX
    :param numbers: list o numbers to format
    :return: return number formatted to save in LaTex
    '''

    formatted = ["$" + "{:.2E}".
        format(float(n)).replace("+0", "").replace("-0", "-"). replace("E", " \! \cdot 10^{") + "}$" for n in numbers]
    return formatted

def procesIndv(i, sep):
    '''
    Process individual to save in fie
    :param i: individual
    :param sep: separator needed to save in file
    :return: individuals processed
    '''
    k = [str(np.round(k, decimals = 2)) for k in i.K]
    f = [str(np.round(a, decimals = 4)) for a in i.f]
    res = sep.join(k + f)
    return res

def processForLatexSummary(med, best, worst, sep=" & "):
    '''
    Process data to generate a line to save in the Latex summary
    :param med: median
    :param best: best result
    :param worst: worst result
    :param sep: separator to save in file
    :return: str composition
    '''
    return sep.join(map(str, format_numbers(med))) + \
           sep + sep.join(format_numbers(best.f)) + sep + sep.join(format_numbers(worst.f))

def processForSummary(med, best, worst, sep="; "):
    '''
    Process data to generate a line to save in the csv summary
    :param med: median
    :param best: best result
    :param worst: worst result
    :param sep: separator to save in file
    :return: str composition
    '''
    return sep.join(map(str,med)) + sep + procesIndv(best,' ;') \
           + sep + procesIndv(worst,' ;')

def saveTableLatex(fileName, experiment, medList, indvList):
    '''
    Save results in LaTeX format
    :param fileName: name of the LaTeX file
    :param experiment: name of the experimetn
    :param medList: list of medians values
    :param indvList: list of individuals
    :return:
    '''
    fileName.write(experiment.name + ' & ' +
               processForLatexSummary(np.around(np.median(medList, axis=0), decimals=4),
                                     indvList[0], indvList[-1]) + ' \\\\  \hline \n')

def saveResultsCSV(fileName, experiment, medList, indvList):
    '''
    Save results in csv format
    :param fileName: name of the csv file
    :param experiment: name of the experiment
    :param medList: list of medians values
    :param indvList: list of individuals
    :return:
    '''
    fileName.write(experiment.name + ' - ' + experiment.info +
                            processForSummary(np.around(np.median(medList, axis=0), decimals=4),
                                           indvList[0], indvList[-1], "; ") + '\n')

def saveResults(experiment, indvList, medList, fileCSV, fileLatex, fileExperiment):
    '''
    Save results i the LaTex and csv summaries and in the experiment csv file
    :param experiment: name of the experiment
    :param medList: list of medians values
    :param indvList: list of individuals
    :param fileCSV: name of the summary csv file
    :param fileLatex: name of the summary LaTeX file
    :param fileExperiment:  name of the experiment csv file
    :return:
    '''
    saveResultsCSV(fileCSV, experiment, medList, indvList)
    saveResultsCSV(fileExperiment, experiment, medList, indvList)
    saveTableLatex(fileLatex, experiment, medList, indvList)
    fileCSV.close()
    fileLatex.close()
