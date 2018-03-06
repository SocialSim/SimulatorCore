class IndependentAction():
    '''
    A simple data structure to hold agent's probabilitiy of generating an independent action.
    '''

    def __init__(self, agentId, actionType, objectId, prob):
        self.agentId = agentId
        self.actionType = actionType
        self.objectId = objectId
        self.prob = prob

        assert (0.0 <= prob <= 1.0)

def IndependentActionSerializer(obj):
    if isinstance(obj, IndependentAction):
        serial = str(obj)
        return serial
    else:
        raise TypeError ("Type not serializable")
