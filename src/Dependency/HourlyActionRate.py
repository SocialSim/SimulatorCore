class HourlyActionRate():
    '''
    A simple data structure to hold an agent's action rate each hour of a day. This time-dependent action is independent of other agents' actions.
    '''

    def __init__(self, agentId, activityLevel, probs):
        '''
        Data sturucure for user's type-specific hourly action distribution.
        :param agentId: user Id
        :param activityLevel: indicate how many actions this user perform for this type per day
        :param actionType: the event Type
        :param probs: probability distribution over each hour of one day
        '''
        self.agentId = agentId
        self.dailyActivityLevel = activityLevel
        self.probs = list(probs)

        # Make sure probs is a proper distribution
        assert (round(sum(probs), 6), 1.0)
        assert (all(0.0 <= prob <= 1.0 for prob in probs))
        assert (len(probs) == 24)

    def __str__(self):
        result = "%s %s " % (str(self.agentId), str(self.dailyActivityLevel)) 
        for prob in self.probs:
            result += "%s " % prob
        return result

    def setActivityLevel(self, activityLevel):
        self.dailyActivityLevel = activityLevel

    def getAgentId(self):
        return self.agentId

    def getActivityLevel(self):
        return self.dailyActivityLevel

    def getProbs(self):
        return self.probs

def HourlyActionRateSerializer(obj):
    if isinstance(obj, HourlyActionRate):
        serial = str(obj)
        return serial
    else:
        raise TypeError ("Type not serializable")
