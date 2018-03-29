import numpy as np

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

    def __str__(self):
        result = "%s %s\n" % (str(self.agentId), str(len(self.objectIds)))
        for i in range(0, len(self.objectIds)):
            result += "%s %s\n" % (str(self.objectIds[i]), str(self.probs[i]))
        return result

    def addObject(self, objectId):
        self.objectIds.append(objectId)
        self.probs.append(min(self.probs))
        self.probs = list(np.array(self.probs) / (1 + min(self.probs)))

    def deleteObject(self, objectId):
        index = self.objectIds.index(objectId)
        prob = self.probs[index]
        self.objectIds.pop(index)
        self.probs.pop(index)
        if prob < 1:
            self.probs = list(np.array(self.probs) / (1 - prob))

    def getAgentId(self):
        return self.agentId

    def getObjectIds(self):
        return self.objectIds

    def getProbs(self):
        return self.probs

def ObjectPreferenceSerialier(obj):
    if isinstance(obj, ObjectPreference):
        serial = str(obj)
        return serial
    else:
        raise TypeError ("Type not serializable")
