import os

class BaseResultAnalyzer:
    def __init__(self, pathToResults, resultPred, analysisLogic, accumLogic, accumulator):
        self.result_path = pathToResults
        self.resultPred = resultPred
        self.analysisLogic = analysisLogic
        self.accumLogic = accumLogic #analysisResults -> accumulator -> accumulator
        self.accumulator = accumulator
        
    #iterate through directory, and yield filenames of result files.
    #resultPred is a function that returns true if the file name is the desired result file.
    def iterResults(self, resultPred):
        for item_name in os.listdir(self.result_path):
            if resultPred(item_name):
                yield item_name

    def iterAnalysis(self, analysisLogic):
        for filename in self.iterResults(self.resultPred):            
            resultFile = open('filename', 'r')
            analysisResults = analysisLogic(resultFile)
            resultFile.close()
            yield analysisResults
            
    def analyzeAll(self):
        for analysisData in self.iterAnalysis(self.analysisLogic):
            self.accumLogic(analysisData, self.accumulator)
        return self.accumulator
            
