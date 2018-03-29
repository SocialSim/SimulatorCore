import common.analysisArgParser as argparser
from AnalysisLib.AnalysisLib import AnalysisLib
from AnalysisLib.IndependentAnalysisLib import IndependentAnalysisLib
from AnalysisLib.ClusIndependentAnalysisLib import ClusIndependentAnalysisLib
import time

def main():
    start = time.time()
    argparser.analysisArgParser()
    analysisLib = IndependentAnalysisLib.getInstance()
    analysisLib.storeStatistics()
    end = time.time()
    print("Analyzing time: %f"%(end - start))

if __name__ == "__main__":
    main()
