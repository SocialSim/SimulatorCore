import argparse

def parseArguments():
    global sargs
    parser = argparse.ArgumentParser(description='Simulation Argument Parser')

    parser.add_argument('--dataset', type = str,
        help='the dataset file of the interested social network', required=True)

    sargs = parser.parse_args()

