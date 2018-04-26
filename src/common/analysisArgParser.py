import argparse

def analysisArgParser():
    global sargs
    parser = argparse.ArgumentParser(description='Analysis Library Argument Parser')

    parser.add_argument('--dataset', type = str,
        help='The dataset file of the interested social network', required=True)
    parser.add_argument('--delim', type = str, default = ' ', 
        help='Delimiter to for events in dataset', required=False)

    sargs = parser.parse_args()

