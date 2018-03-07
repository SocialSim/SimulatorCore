from scipy.stats import rv_discrete
import random


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
        
        objectIndexes = [i for i in range(len(objectPreference.objectIds))]
        rv = rv_discrete(
            values=(objectIndexes, objectPreference.probs))

        for hourlyActionRate in hourlyActionRates:  #Consider each type of actions independently
            if sum(hourlyActionRate.probs) == 0: #No record on this type of actions.
                continue
            prob = hourlyActionRate.probs[currentTime % 24]
            if random.random() <= prob:  #He will adopt an action of this type
                agentId = hourlyActionRate.agentId
                objectId = objectPreference.objectIds[rv.rvs(size=1)[0]]  # Get 1 sample the distribution
                actionType = hourlyActionRate.actionType
                event = [
                    agentId, objectId, actionType, currentTime,
                    currentTime + unitTime
                ]
                events.append(event)

        return events
