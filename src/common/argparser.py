import argparse

sargs = None

def parseArguments():
    global sargs
    parser = argparse.ArgumentParser(description='Simulation Argument Parser')

    sargs = parser.parse_args()

