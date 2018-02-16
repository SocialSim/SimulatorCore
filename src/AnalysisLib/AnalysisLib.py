from Dependency.IndependentAction import IndependentAction
import json
# retrieve dists at getIndendentProbOfAgent through data cube
push_dist = [0,0,0,0,0,0,0,0,0,0.1,0.2,0.2,0.1,0.1,0.1,0.1,0.1,0.0,0.0,0,0,0,0,0]
star_dist = [0,0,0,0,0,0,0,0,0,0.2,0.1,0.1,0.2,0.1,0.1,0.1,0.1,0.0,0.0,0,0,0,0,0]

class AnalysisLib:

    def __init__(self, fname):
        self.attributes = self.loadAttributes(fname)
    
    # Note: put assertion because probability should be between 0 and 1
    def getIndendentProbOfAgent(self, agentId, objId, actionType, timeStep):
        # here is where you can access the data cube to return specific probabilities
        # pattern cube probabilities require agentId, objId, actionType, and timeStep

        if actionType == "push":
            return IndependentAction(agentId, actionType, objId, push_dist[timeStep])
        elif actionType == "star":
            return IndependentAction(agentId, actionType, objId, star_dist[timeStep])
        else:
            return IndependentAction(agentId, actionType, objId, push_dist[timeStep])

    def getAttributes(self): # return config data
        return self.attributes

    def getIds(self, target_type): # return list of ids of target type from config data
        id_list = []
        for attributes in self.attributes[target_type]["attributes"]:
            id_list.append(attributes["id"])
        return id_list

    def getActions(self):
        return self.attributes["actions"]

    def loadAttributes(self, fname):
        with open(fname) as data_file:
            data = json.load(data_file)
        return data
    
    @staticmethod
    def getAgentTimeDependentActions(agentId):
        return None
        
    @staticmethod
    def getAgentDependentActions(agentID):
        return None
