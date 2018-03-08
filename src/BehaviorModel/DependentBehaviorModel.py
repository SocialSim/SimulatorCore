from scipy.stats import rv_discrete
from DependentEventLogger.DependentEventLogger import DependentEventLogger
import random
import numpy as np
from common.event import Event


class DependentBehaviorModel():
    '''
    This class simulate the Independent Cascade(IC) Model. At each timestamp, each "active" user will have an
    independent probability to infect his inactive neighbors.

    Assumption: Each user will perform at most one dependent action at each timestamp(one hour initially).

    Since when we compute the dependency between users, we do not distinguish different event types and objects, we set
    the resulted-action the same type as the action it depends on; with the object ditributed same as his object
    preference.

    TODO: We probably need to find the dependencies between different event types; so that we can better decide the
    event type of dependnet actions.

    The ultimate process of decide a dependent actions:
    1) We first decide whether this user will perform a dependent action.
    2) Acoording to the dependency between types, decide which type of action he will perform.
    3) Choose an object to perform action on according to his object preference.
    '''

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

        dependentEventLogger = DependentEventLogger.getInstance()

        objectIndexes = [i for i in range(len(objectPreference.objectIds))]
        rv = rv_discrete(
            values=(objectIndexes, objectPreference.probs))

        if not userDependency.depUserIds: # No dependency for this user
            return events

        noDenpendentActionProb = 1
        dependentEventTypeScore = {}
        for eventType in DependentBehaviorModel.eventTypes:
                dependentEventTypeScore[eventType] = 0.0

        for depUserId in userDependency.depUserIds:  # Consider each pairwise dependency independently
            dependentProb = userDependency.userDependency[depUserId]
            performedAction = False

            #First check if the dependent user performed action during the dpendency window.
            for timestamp in np.arange(currentTime - dependencyLength, currentTime, unitTime):
                if timestamp < 0:
                    continue
                for eventType in DependentBehaviorModel.eventTypes:
                    if dependentEventLogger.checkUserEventAtTime(depUserId, eventType, timestamp):
                        dependentEventTypeScore[eventType] += dependentProb
                        if not performedAction:
                            performedAction = True

            if performedAction:
                noDenpendentActionProb *= (1 - dependentProb)

        if noDenpendentActionProb < 1:
            actionProb = 1 - noDenpendentActionProb
            if random.random() <= actionProb:  # He will adopt an action of this type
                userId = userDependency.userId  # ID of this user, but not the dependent user.
                objectId = objectPreference.objectIds[rv.rvs(size=1)[0]]  # Get 1 sample the distribution
                #Select the event type with greateset event type score
                actionType = max(dependentEventTypeScore, key=dependentEventTypeScore.get)
                event = Event(userID = userId,
                        objID = objectId,
                        eventType = actionType,
                        timestamp = currentTime)
                events.append(event)

        return events
