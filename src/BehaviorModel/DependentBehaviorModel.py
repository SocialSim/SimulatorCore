from scipy.stats import rv_discrete
from DependencyLogger import DependencyLogger
import random


class DependentBehaviorModel():
    dependencyLength = 50
    eventTypes = ["GITHUB_PULL_REQUEST", "GITHUB_PUSH"]

    def __init__(self):
        pass

    @staticmethod
    def evaluate(userDependency, dependencyLength, dependencyLogger, currentTime, unitTime):
        '''
        Decide user action performed an dependent coin on object by flipping a coin.

        :param hourlyActionRates: list of agent's HourlyActionRate instance, each instance corresponding to one actionType
        :param objectPreference: agent's preference over objects she touches.

        :return: a list of events
        '''

        events = []

        rv = rv_discrete(
            values=(userDependency.depUserIds, userDependency.depUserProbs))

        if not userDependency.depUserIds:
            return

        for depUserId in userDependency.depUserIds:  # Consider each pairwise dependency independently
            index = userDependency.depUserIds.index(depUserId)
            prob = userDependency.depUserProbs[index]
            dependentEventFlag = {"GITHUB_PULL_REQUEST": False, "GITHUB_PUSH": False}
            for timestamp in range(currentTime-dependencyLength, currentTime, unitTime):
                for eventType in DependentBehaviorModel.eventTypes:
                    if dependencyLogger.checkUserEventAtTime(depUserId, eventType, timestamp):
                        dependentEventFlag[eventType] = True
            for eventType in DependentBehaviorModel.eventTypes:
                if dependentEventFlag[eventType]:
                    if random.random() <= prob:  # He will adopt an action of this type
                        agentId = userDependency.userId
                        objectId = rv.rvs(size=1)[0]  #TODO: set the same object as you dependent user did.
                        actionType = eventType
                        event = [
                            agentId, objectId, actionType, currentTime,
                            currentTime + unitTime
                        ]
                        events.append(event)

        return events
