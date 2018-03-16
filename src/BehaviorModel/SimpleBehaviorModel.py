import random
import hashlib
import numpy as np
from scipy.stats import rv_discrete
from common.event import Event
from common.simulationTime import SimulationTime


class SimpleBehaviorModel():

    def __init__(self):
        pass

    @staticmethod
    def evaluate(hourlyActionRates, objectPreference):
        '''
        Decide user action performed on object by flipping a coin.

        :param hourlyActionRates: list of agent's HourlyActionRate instance, each instance corresponding to one actionType
        :param objectPreference: agent's preference over objects she touches.

        :return: a list of events
        '''

        events = []
        
        objectIndexes = np.arange(len(objectPreference.getObjectIds()))
        probs = objectPreference.getProbs()
        agentId = objectPreference.getAgentId()
        objectIds = objectPreference.getObjectIds()
        rv = rv_discrete(values=(objectIndexes, probs))

        for hourlyActionRate in hourlyActionRates:  #Consider each type of actions independently

            actionType = hourlyActionRate.getaActionType()
            dailyActivityLevel = int(round(hourlyActionRate.getActivityLevel())) # How many actions of this type this user may take per day?
            if sum(hourlyActionRate.probs) == 0: #No record on this type of actions.
                continue
            if dailyActivityLevel == 0:
                continue
            currentHour = SimulationTime.getHour()
            prob = hourlyActionRate.probs[currentHour]

            while dailyActivityLevel > 0:
                if dailyActivityLevel < 1:
                    prob *= dailyActivityLevel
                if random.random() <= prob:  # He will adopt an action of this type
                    currentTime = SimulationTime.getIsoTime()
                    if actionType == "CreateEvent":
                        # Generate a random ID for the new object.
                        objectName = agentId + str(currentTime) + str(random.randint(0, 100))
                        objectId = str(hashlib.md5(objectName).hexdigest())[0:22]
                    else:
                        objectId = objectIds[rv.rvs(size=1)[0]]  # Get 1 sample the distribution
                    timeShift = np.random.randint(0, 3600)
                    eventTime = SimulationTime.getIsoTime(timeShift)
                    event = Event(userID = agentId,
                        objID = objectId,
                        eventType = actionType,
                        timestamp = eventTime)
                    events.append(event)

                dailyActivityLevel -= 1

        return events
