class AnalysisLib(object):
    def __init__(self):
        # set up connection to analysis library we choose
        pass

    def getListOfAgentID(self):
        pass

    def getListOfObjID(self):
        pass

    # data structure looks like
    # {obj_id1: {"push": [], "pull": []}, obj_id2: {"push": [0.1, 0.2, 0.7], "pull": [0.2, 0.3, 0.9]}}
    # Note: put assertion because probability should be between 0 and 1
    def getIndendentProbOfAgent(self, agentID, actionType):
        pass

    def getDependentProbOfAgent(self, agentID):
        pass

    # Discuss with Tarek how do we parse and query attributes
    def getAttributesOfAgent(self, agentID):
        pass

    def getAttributesOfObj(self, objID):
        pass

