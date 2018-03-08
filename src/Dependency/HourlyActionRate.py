class HourlyActionRate():
    '''
    A simple data structure to hold an agent's action rate each hour of a day. This time-dependent action is independent of other agents' actions.
    '''

    def __init__(self, agentId, activityLevel, actionType, probs):
        '''
        :param probs: array of time-dependent rate of action. Example: the probability of agent <agentId> generating action <actionType> on some object at 8am is probs[7].
        '''

        self.agentId = agentId
        self.activityLevel = activityLevel
        self.actionType = actionType
        self.probs = list(probs)

        # Make sure probs is a proper distribution
        assert (round(sum(probs), 6), 1.0)
        assert (all(0.0 <= prob <= 1.0 for prob in probs))
        assert (len(probs) == 24)

    def __str__(self):
        return "{%s %s %s %s}" % (str(self.agentId), str(self.activityLevel), 
                str(self.actionType), str(self.probs))

def HourlyActionRateSerializer(obj):
    if isinstance(obj, HourlyActionRate):
        serial = str(obj)
        return serial
    else:
        raise TypeError ("Type not serializable")
