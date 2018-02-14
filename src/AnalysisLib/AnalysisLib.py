from utils import utils

# retrieve dists at getIndependentProofOfAgent through data cube
push_dist = [0,0,0,0,0,0,0,0,0,0.1,0.2,0.2,0.1,0.1,0.1,0.1,0.1,0.0,0.0,0,0,0,0,0]
star_dist = [0,0,0,0,0,0,0,0,0,0.2,0.1,0.1,0.2,0.1,0.1,0.1,0.1,0.0,0.0,0,0,0,0,0]

class AnalysisLib:
    def __init__(self):
        # set up connection to analysis library we choose
        self.agent_id = utils.get_ids("agents")
        self.obj_id = utils.get_ids("objects")

    def getListOfAgentID(self):
        return self.agent_id
    
    def getListOfObjID(self):
        return self.obj_id
    
    # data structure looks like
    # {obj_id1: {"push": [], "pull": []}, obj_id2: {"push": [0.1, 0.2, 0.7], "pull": [0.2, 0.3, 0.9]}}
    # Note: put assertion because probability should be between 0 and 1
    def getIndendentProbOfAgent(self, agentId):
        # here is where you can access the data cube to return specific probabilities

        # define temp independent probabilities
        ind_prob = {id: {0: {"push": push_dist, "star": star_dist}, 1: {"push": push_dist, "star": star_dist}} for id in self.agent_id}

        return ind_prob[agentId]
        
    
    def getDependentProbOfAgent(self, agentID):
        pass
    
    # Discuss with Tarek how do we parse and query attributes
    def getAttributesOfAgent(self, agentID):
        pass
    
    def getAttributesOfObj(self, objID):
        pass
