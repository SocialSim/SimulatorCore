import random
import hashlib
import numpy as np
from scipy.stats import rv_discrete
from common.event import Event
from common.simulationTime import SimulationTime
from common.const import *
from common.discreteSample import sample


class SimpleBehaviorModel():

    def __init__(self):
        pass

    @staticmethod
    def userEvaluate(userId, hourlyActionRate, objectIds, cumObjectPreference, cumTypeDistribution):
        '''
        Used for user agent. Decide user action performed on object by flipping a coin.
        '''

        events = []

        dailyActivityLevel = hourlyActionRate.getActivityLevel()

        currentHour = SimulationTime.getHour()
        prob = hourlyActionRate.probs[currentHour]

        while dailyActivityLevel > 0:
            if dailyActivityLevel < 1:
                prob *= dailyActivityLevel
            if random.random() <= prob:  # He will adopt an action
                actionType = sample(CORE_EVENT_TYPES, cumTypeDistribution)

                if actionType == "CreateEvent":
                    # Generate a random ID for the new object.
                    objectName = userId.join(str(random.random()))
                    objectId = str(hashlib.md5(objectName).hexdigest())[0:22]
                else:
                    objectId = sample(objectIds, cumObjectPreference)  # Get 1 sample the distribution

                timeShift = np.random.randint(0, 3600)
                event = Event(userID=userId,
                              objID=objectId,
                              eventType=actionType,
                              timestamp=SimulationTime.getIsoTime(timeShift))
                events.append(event)

            dailyActivityLevel -= 1

        return events

    @staticmethod
    def clusterEvaluate(clusterAgent, hourlyActionRate, cumTypeDistribution, memberObjectPreferences,
                        memberCumObjectPreference):
        '''
        Used for cluster agent. Decide user action performed on object by flipping a coin.
        '''

        events = []

        dailyActivityLevel = hourlyActionRate.getActivityLevel()

        currentHour = SimulationTime.getHour()
        prob = hourlyActionRate.probs[currentHour]

        while dailyActivityLevel > 0:
            if dailyActivityLevel < 1:
                prob *= dailyActivityLevel
            if random.random() <= prob:  # He will adopt an action
                actionType = sample(CORE_EVENT_TYPES, cumTypeDistribution)
                userId = clusterAgent.scheduleUser()

                if actionType == "CreateEvent":
                    # Generate a random ID for the new object.
                    objectName = userId.join(str(random.random()))
                    objectId = str(hashlib.md5(objectName).hexdigest())[0:22]
                else:
                    objectId = sample(memberObjectPreferences[userId].objectIds,
                                      memberCumObjectPreference[userId])

                timeShift = np.random.randint(0, 3600)
                event = Event(userID=userId,
                              objID=objectId,
                              eventType=actionType,
                              timestamp=SimulationTime.getIsoTime(timeShift))
                events.append(event)

            dailyActivityLevel -= 1

        return events
