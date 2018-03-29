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
        return "{%s %s}" % (str(self.agentId), str(self.probs))

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
