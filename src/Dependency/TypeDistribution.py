class TypeDistribution():
    '''
    A simple data structure to hold an agent's action distribution among different event types.
    '''

    def __init__(self, agentId, probs):

        self.agentId = agentId
        self.probs = list(probs)

        # Make sure probs is a proper distribution
        assert (round(sum(probs), 6), 1.0)
        assert (all(0.0 <= prob <= 1.0 for prob in probs))

    def __str__(self):
        result = "%s " % (str(self.agentId))
        for prob in self.probs:
            result += "%s " % str(prob)
        result += "\n"
        return result

    def getAgentId(self):
        return self.agentId

    def getProbs(self):
        return self.probs

def TypeDistributionSerializer(obj):
    if isinstance(obj, TypeDistribution):
        serial = str(obj)
        return serial
    else:
        raise TypeError ("Type not serializable")
