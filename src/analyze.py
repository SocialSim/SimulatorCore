import common.analysisArgParser as argparser
from AnalysisLib.AnalysisLib import AnalysisLib
from AnalysisLib.IndependentAnalysisLib import IndependentAnalysisLib

def main():
    argparser.analysisArgParser()
    IndependentAnalysisLib()

if __name__ == "__main__":
    main()
