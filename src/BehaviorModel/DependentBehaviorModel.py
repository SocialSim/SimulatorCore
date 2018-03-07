from scipy.stats import rv_discrete
from DependencyLogger.DependencyLogger import DependencyLogger
import random
import numpy as np


class DependentBehaviorModel():

    eventTypes = ["CommitCommentEvent", "CreateEvent", "DeleteEvent", "ForkEvent", "IssueCommentEvent",
                  "IssuesEvent", "PullRequestEvent", "PushEvent", "WatchEvent", "PublicEvent",
                  "MemberEvent", "GollumEvent", "ReleaseEvent", "PullRequestReviewCommentEvent"]

    def __init__(self):
        pass

    @staticmethod
    def evaluate(userDependency, dependencyLength, objectPreference, currentTime, unitTime):
        '''
        Simmulate the user dependent actions according to his dependency relationship and
        the actions of his dependent users.
        :param userDependency: the dependency relationships of the given user
        :param dependencyLength: the length of dependnecy we consider here, a measure on time.
        :param dependencyLogger: the log of the simulated events we need to query
        :param objectPreference: the preference among objects of this given user.
        :param currentTime: current time step
        :param unitTime: length of time of each step

        :return: the simulated dependent events
        '''
        events = []

        dependencyLogger = DependencyLogger.getInstance()

        objectIndexes = [i for i in range(len(objectPreference.objectIds))]
        rv = rv_discrete(
            values=(objectIndexes, objectPreference.probs))

        if not userDependency.depUserIds: # No dependency for this user
            return events

        for depUserId in userDependency.depUserIds:  # Consider each pairwise dependency independently
            prob = userDependency.userDependency[depUserId]
            dependentEventFlag = {}
            for eventType in DependentBehaviorModel.eventTypes:
                dependentEventFlag[eventType] = False
            #First check if the dependent user performed action during the dpendency window.
            for timestamp in np.arange(currentTime - dependencyLength, currentTime, unitTime):
                if timestamp < 0:
                    continue
                for eventType in DependentBehaviorModel.eventTypes:
                    if dependencyLogger.checkUserEventAtTime(depUserId, eventType, timestamp):
                        dependentEventFlag[eventType] = True
            #This user will perform a same-type action as his dependent user based on his object preference
            for eventType in DependentBehaviorModel.eventTypes:
                if dependentEventFlag[eventType]:
                    if random.random() <= prob:  # He will adopt an action of this type
                        agentId = userDependency.userId #ID of this user, but not the dependent user.
                        objectId = objectPreference.objectIds[rv.rvs(size=1)[0]]  # Get 1 sample the distribution
                        actionType = eventType
                        event = [
                            agentId, objectId, actionType, currentTime,
                            currentTime + unitTime
                        ]
                        events.append(event)

        return events
