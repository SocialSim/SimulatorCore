from Dependency.IndependentAction import IndependentAction
from utils import utils
from collections import OrderedDict
from AnalysisTools import PatternCube

import json

class AnalysisLib:

    def __init__(self, fname):
        # load initial agent attributes
        self.attributes = self.loadAttributes(fname)

        # load data cube
        self.cube = PatternCube.pattern_cube()
    
    # Note: put assertion because probability should be between 0 and 1
    def getIndendentProbOfAgent(self, agentId, objId, actionType, timeStep):
        # here is where you can access the data cube to return specific probabilities

        # get probability distribution from data cube
        agent_attributes = self.attributes["agents"]["attributes"][utils.get_dict_id_index(agentId, self.attributes["agents"]["attributes"])]
        object_attributes = self.attributes["objects"]["attributes"][utils.get_dict_id_index(objId, self.attributes["objects"]["attributes"])]
        dist = self.cube.get_independent_probability(agent_attributes, object_attributes, actionType)

        if actionType == "push":
            return IndependentAction(agentId, actionType, objId, dist[timeStep])
        elif actionType == "star":
            return IndependentAction(agentId, actionType, objId, dist[timeStep])
        else:
            return IndependentAction(agentId, actionType, objId, dist[timeStep])

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
            data = json.load(data_file, object_pairs_hook=OrderedDict)
        return data
    
    @staticmethod
    def getAgentTimeDependentActions(agentId):
        return None
        
    @staticmethod
    def getAgentDependentActions(agentID):
        return None
