import sys
import common.argparser as argparser
from SimulatorCore.TimeBasedSimulator import TimeBasedSimulator

def evaluate(simulator):
    from SocialSimEvaluationEngine.metrics.metrics.SocialSimEvaluationEngine import SocialSimEvaluationEngine
    evaluationEngine = SocialSimEvaluationEngine()
    for event in simulator.eventHistory:
        evaluationEngine.push(event)

    sys.stdout = open('evaluation.result', 'w')

    topkUser = evaluationEngine.evaluateQuestion27(5)
    topkUser = list(topkUser.index.values)
    print type(topkUser)
    print type(simulator.getAllUserIDs())
    print topkUser[0]
    print simulator.getAllUserIDs()[0]
    evaluationEngine.evaluateQuestion20(simulator.getAllUserIDs(), False)
    evaluationEngine.evaluateQuestion20(simulator.getAllUserIDs(), True)
    evaluationEngine.evaluateQuestion20(topkUser, True)
    evaluationEngine.evaluateQuestion18(topkUser, True)
    evaluationEngine.evaluateQuestion29bc(topkUser, 5, True)

    # evaluationEngine.evaluateQuestion18(simulator.getAllUserIDs(), True)
    # evaluationEngine.evaluateQuestion26a("GITHUB_PUSH")
    # evaluationEngine.evaluateQuestion26b(10)
    # evaluationEngine.evaluateQuestion28Gini()
    # evaluationEngine.evaluateQuestion28Palma()
    # evaluationEngine.evaluateQuestion29bc(simulator.getAllUserIDs(), 10)
    # evaluationEngine.evaluateQuestion29('s')

if __name__ == "__main__":
    evaluate()
