class ObjectPreference():
    '''
    A simple data structure to hold an agent's preference over the objects she touches.
    '''

    def __init__(self, agentId, objectIds, probs):
        self.agentId = agentId
        self.objectIds = objectIds
        self.probs = list(probs)

        assert (len(objectIds) == len(probs))
        assert (round(sum(probs), 6), 1.0)
        assert (all(0.0 <= prob <= 1.0 for prob in probs))

def ObjectPreferenceSerialier(obj):
    if isinstance(obj, ObjectPreference):
        serial = str(obj)
        return serial
    else:
        raise TypeError ("Type not serializable")
