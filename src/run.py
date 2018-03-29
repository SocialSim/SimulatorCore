import logging
import sys
import time

import common.argparser as argparser
from SimulatorCore.TimeBasedSimulator import TimeBasedSimulator
from AgentBuilder.AgentBuilder import AgentBuilder
from Agent.GithubChallenge.SimpleUserAgent import SimpleUserAgent
from Agent.GithubChallenge.DependentUserAgent import DependentUserAgent
from Agent.GithubChallenge.SimpleObjectAgent import SimpleObjectAgent
from Agent.GithubChallenge.SimpleUserClusterAgent import SimpleUserClusterAgent
from common.const import *
from common.simulationTime import SimulationTime
import Evaluator.Evaluator as evaluator

def main():

    argparser.parseArguments()

    # Set the timezone as UTC
    os.environ['TZ'] = "UTC"
    time.tzset()

    logging.basicConfig(stream=sys.stderr,
                        format='[%(asctime)s] %(name)s:%(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    logger = logging.getLogger("main")
    
    logger.info("Init and config agent builder...")
    agentBuilder = AgentBuilder(UserAgentModel=SimpleUserAgent,
                                ObjectAgentModel=SimpleObjectAgent,
                                ClusterAgentModel=SimpleUserClusterAgent)
    userAgents, objectAgents, clusterAgents = agentBuilder.build()

    logger.info("Init and config simulation setting...")
    SimulationTime.getInstance(year=2015, month=2, day=1, hour=0, minute=0, second=0)
    simulator = TimeBasedSimulator( userAgents=userAgents,
                                    objectAgents=objectAgents,
                                    clusterAgents=clusterAgents,
                                    simulationLength=24*28,
                                    unitTime="hour")

    logger.info("Start simulation...")
    start = time.time()
    simulator.run()
    end = time.time()
    logger.info("Simulation time: %f s"%(end - start))
    simulator.saveLog()

    if argparser.sargs.evaluation:
        logger.info("Evaluating...")
        groundTruthFile = DATAPATH + "event_2015-01-25_31.txt"
        evaluator.evaluate(simulator, groundTruthFile)

if __name__ == "__main__":
    main()
