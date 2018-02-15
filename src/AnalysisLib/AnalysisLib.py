test_dist = [0,0,0,0,0,0,0,0,0,0.1,0.2,0.2,0.1,0.1,0.1,0.1,0.1,0.0,0.0,0,0,0,0,0]


class AnalysisLib:
    def __init__(self):
        # set up connection to analysis library we choose
        self.agentIds = [0,1,2,3,4]
        self.objectIds = [0]
        self.ind_prob = {id:{0:{"push":test_dist}} for id in self.agentIds}

    def getListOfAgentIds(self):
        return self.agentIds
    
    def getListOfObjIds(self):
        return self.objIds
    
    # data structure looks like
    # {obj_id1: {"push": [], "pull": []}, obj_id2: {"push": [0.1, 0.2, 0.7], "pull": [0.2, 0.3, 0.9]}}
    # Note: put assertion because probability should be between 0 and 1
    def getIndendentProbOfAgent(self, agentId):
        return self.ind_prob[agentId]
        
    
    def getDependentProbOfAgent(self, agentID):
        pass
    
    # Discuss with Tarek how do we parse and query attributes
    def getAttributesOfAgent(self, agentID):
        pass
    
    def getAttributesOfObj(self, objID):
        pass
