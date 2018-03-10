import sys

from EvaluationEngine import EvaluationEngine
from common.const import *
import time


def eventSplit(line):
    '''
    Given a line of input, extract the attributes.
    :param line: A line of input with format #Event format: (eventTime, objectId, userId)
    :return:
    '''
    event = line.split(" ")
    eventTime = int(event[0])
    objectId = event[1]
    userId = event[2]
    eventType = event[3]
    return eventTime, objectId, userId, eventType

def evaluate(simulator, groundTruthFile):
    start = time.time()
    evaluationEngine = EvaluationEngine()

    for event in simulator.eventHistory:
        evaluationEngine.push(event)

    with open(groundTruthFile, "rb") as input:
        for line in input:
            line = line.strip('\n')
            eventTime, objectId, userId, eventType = eventSplit(line)
            evaluationEngine.groundTruthPush([eventTime, objectId, userId, eventType])

    sys.stdout = open('evaluation.result', 'w')

    topkUser = evaluationEngine.evaluateQuestion27(10)
    topkUser = list(topkUser.index.values)
    # print type(topkUser)
    # print type(simulator.getAllUserIDs())
    # print topkUser[0]
    # print simulator.getAllUserIDs()[0]
    # evaluationEngine.evaluateQuestion20(simulator.getAllUserIDs(), False)
    # evaluationEngine.evaluateQuestion20(simulator.getAllUserIDs(), True)
    # evaluationEngine.evaluateQuestion20(topkUser, True)
    evaluationEngine.evaluateQuestion18(topkUser, False)
    evaluationEngine.evaluateQuestion18(topkUser, True)
    # evaluationEngine.evaluateQuestion29bc(topkUser, 5, True)

    # evaluationEngine.evaluateQuestion18(simulator.getAllUserIDs(), True)
    # evaluationEngine.evaluateQuestion26a("GITHUB_PUSH")
    evaluationEngine.evaluateQuestion26b(10)
    # evaluationEngine.evaluateQuestion28Gini()
    # evaluationEngine.evaluateQuestion28Palma()
    # evaluationEngine.evaluateQuestion29bc(simulator.getAllUserIDs(), 10)
    # evaluationEngine.evaluateQuestion29('s')
    end = time.time()
    print("Evaluation time: %f s"%(end - start))

def offlineEvaluate(SimulationFile, GroundTruthFile):
    start = time.time()
    evaluationEngine = EvaluationEngine()

    with open(SimulationFile, "rb") as file:
        for line in file:
            line = line.strip('\n')
            eventTime, objectId, userId, eventType = eventSplit(line)
            evaluationEngine.simulationPush([eventTime, objectId, userId, eventType])

    with open(GroundTruthFile, "rb") as file:
        for line in file:
            line = line.strip('\n')
            eventTime, objectId, userId, eventType = eventSplit(line)
            evaluationEngine.groundTruthPush([eventTime, objectId, userId, eventType])

    # sys.stdout = open('evaluation.result', 'w')

    topkUser = evaluationEngine.evaluateQuestion27(10)
    topkUser = list(topkUser.index.values)
    # evaluationEngine.evaluateQuestion20(simulator.getAllUserIDs(), False)
    # evaluationEngine.evaluateQuestion20(simulator.getAllUserIDs(), True)
    # evaluationEngine.evaluateQuestion20(topkUser, True)
    evaluationEngine.evaluateQuestion18(topkUser, True)
    # evaluationEngine.evaluateQuestion29bc(topkUser, 5, True)

    # evaluationEngine.evaluateQuestion18(simulator.getAllUserIDs(), True)
    # evaluationEngine.evaluateQuestion26a("PushEvent", True)
    evaluationEngine.evaluateQuestion26b(10, True)
    # evaluationEngine.evaluateQuestion28Gini()
    # evaluationEngine.evaluateQuestion28Palma()
    # evaluationEngine.evaluateQuestion29bc(simulator.getAllUserIDs(), 10)
    # evaluationEngine.evaluateQuestion29('s')
    end = time.time()
    print("Evaluation time: %f s"%(end - start))

if __name__ == "__main__":
    SimulationFile = DATAPATH + "simulated_events.txt"
    GroundTruthFile = DATAPATH + "event_2015-01-25_31.txt"
    offlineEvaluate(SimulationFile, GroundTruthFile)