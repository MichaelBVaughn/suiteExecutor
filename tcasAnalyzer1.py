#!/usr/bin/python
import resultAnalysis
import re

class tcasAcc:
    def __init__(self):
        self.numResults = 0
        self.successfulCompilations = 0
        self.successfulMutantsFile = open("successfulMutants.txt", "w")

    def cleanup(self):
        self.successfulMutantsFile.close()

import pdb
def resultPred(filename):
    return True

def analysisLogic(resultFile):
    target_str = "compilation failed\n"
    statusStr = resultFile.readline()
    successfulCompile = target_str != statusStr
    mutation = resultFile.readlines()
    if successfulCompile:
        mutation.insert(0, statusStr)
    return (successfulCompile, mutation)

def accumLogic(analysisResults, acc):
    if analysisResults[0]:
        acc.successfulCompilations += 1
    acc.numResults += 1
    acc.successfulMutantsFile.write("Mutant +" + str(len(analysisResults[1])))
    acc.successfulMutantsFile.writelines(analysisResults[1])
    return acc


if __name__ == "__main__":
    acc = tcasAcc()
    path = "/u/v/a/vaughn/public/traceAnalysis/tcas/test1/results/"
    analyzer = resultAnalysis.BaseResultAnalyzer(path, resultPred, analysisLogic, accumLogic, acc)
    final = analyzer.analyzeAll()
    final.cleanup()
    print "Total Results: " + str(final.numResults)
    print "Successful Compilations: " + str(final.successfulCompilations)
