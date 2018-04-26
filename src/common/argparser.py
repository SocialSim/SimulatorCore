import argparse

def parseArguments():
    global sargs
    parser = argparse.ArgumentParser(description='Simulation Argument Parser')

    parser.add_argument('--evaluation', action = 'store_true',
        help='whether an evaluation is invoked after simulation. Note, this switch only works when you have evaluation engine under src folder', required=False)

    sargs = parser.parse_args()

