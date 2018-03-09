import common.analysisArgParser as argparser
from AnalysisLib.AnalysisLib import AnalysisLib
from AnalysisLib.IndependentAnalysisLib import IndependentAnalysisLib
import time

def main():
    start = time.time()
    argparser.analysisArgParser()
    IndependentAnalysisLib()
    end = time.time()
    print("Analyze time: %f"%(end - start))

if __name__ == "__main__":
    main()
