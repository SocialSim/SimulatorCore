from Dependency.ObjectPreference import ObjectPreference
from Dependency.HourlyActionRate import HourlyActionRate

class AnalysisLib:
    agentIds = [0,1,2,3,4]
    objectIds = [0,1,2]
    probs = [.2,.3,.5]
    testDist = [0,0,0,0,0,0,0,0,0,0.1,0.2,0.2,0.1,0.1,0.1,0.1,0.1,0.0,0.0,0,0,0,0,0]
    
    def __init__(self):
        pass

    
    @staticmethod
    def getListOfAgentIds():
        return AnalysisLib.agentIds

    
    @staticmethod
    def getListOfObjIds():
        return AnalysisLib.objectIds
    

    @staticmethod
    def getAgentIndependentActions(agentId):
        return None
    
    
    @staticmethod
    def getAgentHourlyActionRate(agentId):
        '''
        :return: a list of HourlyActionRate instances, one for each actionType 
        '''
        
        pullRequestAction = HourlyActionRate(agentId, "GITHUB_PULL_REQUEST", AnalysisLib.testDist) 
        pushAction = HourlyActionRate(agentId, "GITHUB_PUSH", AnalysisLib.testDist) 

        return [pushAction, pullRequestAction]
        

    @staticmethod
    def getAgentObjectPreference(agentId):
        '''
        :return: an ObjectPreference instance
        '''
        objectPreference = ObjectPreference(agentId, AnalysisLib.objectIds, AnalysisLib.probs)
        return objectPreference
    
        
    @staticmethod
    def getAgentDependentActions(agentID):
        return None
    
