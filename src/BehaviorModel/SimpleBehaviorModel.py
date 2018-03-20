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
    def evaluate(hourlyActionRate, objectPreference, typeDistribution):
        '''
        Decide user action performed on object by flipping a coin.

        :param hourlyActionRates: list of agent's HourlyActionRate instance, each instance corresponding to one actionType
        :param objectPreference: agent's preference over objects she touches.

        :return: a list of events
        '''

        events = []

        agentId = objectPreference.getAgentId()

        objectIds = objectPreference.getObjectIds()
        objectProbs = objectPreference.getProbs()
        objectIndexes = np.arange(len(objectIds))
        object_rv = rv_discrete(values=(objectIndexes, objectProbs))

        typeProbs = typeDistribution.probs
        type_rv = rv_discrete(values=(TYPE_INDEX, typeProbs))

        dailyActivityLevel = hourlyActionRate.dailyActivityLevel

        if sum(hourlyActionRate.probs) == 0:
            return events
        if dailyActivityLevel == 0:
            return events

        currentHour = SimulationTime.getHour()
        prob = hourlyActionRate.probs[currentHour]

        while dailyActivityLevel > 0:
            if dailyActivityLevel < 1:
                prob *= dailyActivityLevel
            if random.random() <= prob:  # He will adopt an action
                # currentTime = SimulationTime.getIsoTime()
                actionType = EVENT_TYPEs[type_rv.rvs(size=1)[0]]
                if actionType == "CreateEvent":
                    # Generate a random ID for the new object.
                    objectName = agentId + str(random.randint(0, 1000))
                    objectId = str(hashlib.md5(objectName).hexdigest())[0:22]
                else:
                    objectId = objectIds[object_rv.rvs(size=1)[0]]  # Get 1 sample the distribution
                timeShift = np.random.randint(0, 3600)
                eventTime = SimulationTime.getIsoTime(timeShift)
                event = Event(userID=agentId,
                              objID=objectId,
                              eventType=actionType,
                              timestamp=eventTime)
                events.append(event)

            dailyActivityLevel -= 1

        return events


    @staticmethod
    def evaluate(agentId, hourlyActionRate, objectIds, cumObjectPreference, cumTypeDistribution):
        '''
        Decide user action performed on object by flipping a coin.
        '''

        events = []

        dailyActivityLevel = hourlyActionRate.getActivityLevel()

        currentHour = SimulationTime.getHour()
        prob = hourlyActionRate.probs[currentHour]

        while dailyActivityLevel > 0:
            if dailyActivityLevel < 1:
                prob *= dailyActivityLevel
            if random.random() <= prob:  # He will adopt an action
                actionType = sample(EVENT_TYPEs, cumTypeDistribution)
                if actionType == "CreateEvent":
                    # Generate a random ID for the new object.
                    objectName = agentId + str(random.random())
                    objectId = str(hashlib.md5(objectName).hexdigest())[0:22]
                else:
                    objectId = sample(objectIds, cumObjectPreference)  # Get 1 sample the distribution
                timeShift = np.random.randint(0, 3600)
                eventTime = SimulationTime.getIsoTime(timeShift)
                event = Event(userID=agentId,
                              objID=objectId,
                              eventType=actionType,
                              timestamp=eventTime)
                events.append(event)

            dailyActivityLevel -= 1

        return events
