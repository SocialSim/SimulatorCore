from Dependency.IndependentAction import IndependentAction


class AnalysisLib:
    agentIds = [0,1,2,3,4]
    objectIds = [0]

    
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
        # Hard code for now
        pullRequestAction = IndependentAction(agentId, "GITHUB_PULL_REQUEST", AnalysisLib.objectIds[0], 0.05)
        pushAction = IndependentAction(agentId, "GITHUB_PUSH", AnalysisLib.objectIds[0], 0.1)
        return [pushAction, pullRequestAction]

    
    @staticmethod
    def getAgentTimeDependentActions(agentId):
        return None
        

    @staticmethod
    def getAgentDependentActions(agentID):
        return None
    
