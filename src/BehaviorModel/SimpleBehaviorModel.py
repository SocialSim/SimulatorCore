import random
from scipy.stats import rv_discrete
from common.event import Event


class SimpleBehaviorModel():

    def __init__(self):
        pass

    @staticmethod
    def evaluate(hourlyActionRates, objectPreference, currentTime, unitTime):
        '''
        Decide user action performed on object by flipping a coin.

        :param hourlyActionRates: list of agent's HourlyActionRate instance, each instance corresponding to one actionType
        :param objectPreference: agent's preference over objects she touches.

        :return: a list of events
        '''

        events = []
        
        rv = rv_discrete(
            values=(objectPreference.objectIds, objectPreference.probs))

        for hourlyActionRate in hourlyActionRates:  #Consider each type of actions independently
            prob = hourlyActionRate.probs[currentTime % 24]
            if random.random() <= prob:  #He will adopt an action of this type
                agentId = hourlyActionRate.agentId
                objectId = rv.rvs(size=1)[0]  # Get 1 sample the distribution
                actionType = hourlyActionRate.actionType
                event = Event(userID = agentId,
                        objID = objectId,
                        eventType = actionType,
                        timestamp = currentTime)
                events.append(event)

        return events
