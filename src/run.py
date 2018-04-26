import logging
import sys
import time

import common.argparser as argparser
from SimulatorCore.TimeBasedSimulator import TimeBasedSimulator
from AgentBuilder.AgentBuilder import AgentBuilder
from Agent.GithubChallenge.SimpleUserAgent import SimpleUserAgent
from Agent.GithubChallenge.DependentUserAgent import DependentUserAgent
from Agent.GithubChallenge.SimpleObjectAgent import SimpleObjectAgent
import Evaluator.Evaluator as evaluator

def main():
    start = time.time()

    argparser.parseArguments()

    logging.basicConfig(stream=sys.stderr,
                        format='[%(asctime)s] %(name)s:%(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    logger = logging.getLogger("main")
    
    logger.info("Init and config agent builder...")
    agentBuilder = AgentBuilder(UserAgentModel=SimpleUserAgent,
                                ObjectAgentModel=SimpleObjectAgent)
    userAgents, objectAgents, temporalPreference = agentBuilder.build()

    logger.info("Init and config simulation setting...")
    simulator = TimeBasedSimulator( userAgents=userAgents,
                                    objectAgents=objectAgents,
                                    temporalPreference=temporalPreference,
                                    startTime=0, endTime=24, unitTime=1)

    logger.info("Start simulation...")
    simulator.run()
    simulator.saveLog()
    end = time.time()
    logger.info("Simulation time: %f s"%(end - start))

    if argparser.sargs.evaluation: 
        evaluator.evaluate(simulator)

if __name__ == "__main__":
    main()
