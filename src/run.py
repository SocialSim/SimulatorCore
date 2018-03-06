import logging
import sys

import common.argparser as argparser
from SimulatorCore.TimeBasedSimulator import TimeBasedSimulator
from AgentBuilder.AgentBuilder import AgentBuilder
from Agent.GithubChallenge.SimpleUserAgent import SimpleUserAgent
from Agent.GithubChallenge.DependentUserAgent import DependentUserAgent
from Agent.GithubChallenge.SimpleObjectAgent import SimpleObjectAgent


def main():
    argparser.parseArguments()
    logging.basicConfig(stream=sys.stderr,
                        format='[%(asctime)s] %(name)s:%(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.INFO)
    logger = logging.getLogger("main")
    
    logger.info("Init and config agent builder...")
    # Init and config AgentBuilder
    agentBuilder = AgentBuilder(UserAgentModel=DependentUserAgent,
                                ObjectAgentModel=SimpleObjectAgent)
    userAgents, objectAgents = agentBuilder.build()

    logger.info("Init and config simulation setting...")
    simulator = TimeBasedSimulator( userAgents=userAgents,
                                    objectAgents=objectAgents,
                                    startTime=0, endTime=24, unitTime=1)

    logger.info("Start simulation...")
    simulator.run()

    simulator.showLog()

    # TODO collect data and analyze


if __name__ == "__main__":
    main()
