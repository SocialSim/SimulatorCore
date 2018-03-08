import argparse

def analysisArgParser():
    global sargs
    parser = argparse.ArgumentParser(description='Analysis Library Argument Parser')

    parser.add_argument('--dataset', type = str,
        help='the dataset file of the interested social network', required=True)

    sargs = parser.parse_args()

