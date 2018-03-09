import logging
import sys
import time

import common.argparser as argparser
from SimulatorCore.TimeBasedSimulator import TimeBasedSimulator
from AgentBuilder.AgentBuilder import AgentBuilder
from Agent.GithubChallenge.SimpleUserAgent import SimpleUserAgent
from Agent.GithubChallenge.DependentUserAgent import DependentUserAgent
from Agent.GithubChallenge.SimpleObjectAgent import SimpleObjectAgent


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
    userAgents, objectAgents = agentBuilder.build()

    logger.info("Init and config simulation setting...")
    simulator = TimeBasedSimulator( userAgents=userAgents,
                                    objectAgents=objectAgents,
                                    startTime=0, endTime=24, unitTime=1)

    logger.info("Start simulation...")
    simulator.run()
    end = time.time()
    logger.info("Simulation time: %f s"%(end - start))
    # simulator.showLog()

    if argparser.sargs.evaluation: 
        evaluate(simulator)

def evaluate(simulator):
    from SocialSimEvaluationEngine.metrics.metrics.SocialSimEvaluationEngine import SocialSimEvaluationEngine
    evaluationEngine = SocialSimEvaluationEngine()
    for event in simulator.eventHistory:
        evaluationEngine.push(event)

    sys.stdout = open('evaluation.result', 'w')

    evaluationEngine.evaluateQuestion18(simulator.getAllUserIDs())
    evaluationEngine.evaluateQuestion20(simulator.getAllUserIDs())
    evaluationEngine.evaluateQuestion26a("GITHUB_PUSH")
    evaluationEngine.evaluateQuestion26b(10)
    evaluationEngine.evaluateQuestion27(10)
    evaluationEngine.evaluateQuestion28Gini()
    evaluationEngine.evaluateQuestion28Palma()
    evaluationEngine.evaluateQuestion29bc(simulator.getAllUserIDs(), 10)
    evaluationEngine.evaluateQuestion29('s')

if __name__ == "__main__":
    main()
