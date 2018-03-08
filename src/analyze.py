import common.analysisArgParser as argparser
from AnalysisLib.AnalysisLib import AnalysisLib

def main():
    argparser.analysisArgParser()
    AnalysisLib()

if __name__ == "__main__":
    main()
