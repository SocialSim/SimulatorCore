from Dependency.ObjectPreference import ObjectPreference
from Dependency.HourlyActionRate import HourlyActionRate
import numpy as np

class AnalysisLib:
    agentIds = []
    objectIds = []
    agentObjectPreference = {}
    agentHourlyActionRate = {}
    agentActionCount = {}
    generalObjectPreference = {}
    generalHourlyActionRate = np.array([0.0 for i in range(24)])
    
    def __init__(self):
        with open("../../data/push_short.txt") as file:
            for line in file:
                if not line:
                    break
                else:
                    #Event format: (eventTime,objectId,actorId)
                    event = line.split(",")
                    eventTime = int(event[0])
                    hour = (eventTime/3600)%24
                    objectId = int(event[1])
                    agentId = int(event[2])

                    #Update the agentsIds and his records
                    if agentId not in AnalysisLib.agentIds: #This is a new user.
                        AnalysisLib.agentIds.append(agentId)
                        AnalysisLib.agentActionCount[agentId] = 1

                        #Update the agentHourlyActionRate
                        hourlyActions = np.array([0.0 for i in range(24)])
                        hourlyActions[hour] += 1
                        AnalysisLib.agentHourlyActionRate[agentId] = hourlyActions

                        #Update the agentObjectPreference
                        objectPreference = {objectId: 1.0}
                        AnalysisLib.agentObjectPreference[agentId] = objectPreference
                    else: #Not a new user.
                        AnalysisLib.agentActionCount[agentId] += 1
                        AnalysisLib.agentHourlyActionRate[agentId][hour] += 1
                        if objectId not in AnalysisLib.agentObjectPreference[agentId]: #Did not touch this object before
                            AnalysisLib.agentObjectPreference[agentId][objectId] = 1.0
                        else:
                            AnalysisLib.agentObjectPreference[agentId][objectId] += 1
                    #Update the objectIds
                    if objectId not in AnalysisLib.objectIds:
                        AnalysisLib.objectIds.append(objectId)

                    #Update the generalObjectPreference and generalHourlyActionRate
                    if objectId not in AnalysisLib.generalObjectPreference:
                        AnalysisLib.generalObjectPreference[objectId] = 1.0
                    else:
                        AnalysisLib.generalObjectPreference[objectId] += 1
                    AnalysisLib.generalHourlyActionRate[hour] += 1

        #Update the agentHourActionRate and agentObjectPreference
        for agentId in AnalysisLib.agentIds:
            AnalysisLib.agentHourlyActionRate[agentId] /= AnalysisLib.agentActionCount[agentId]
            for objectId in AnalysisLib.agentObjectPreference[agentId]:
                AnalysisLib.agentObjectPreference[agentId][objectId] /= AnalysisLib.agentActionCount[agentId]

        #Update the generalObjectPreference and generalHourlyActionRate
        totalActions = sum(AnalysisLib.agentActionCount.values())
        AnalysisLib.generalHourlyActionRate /= totalActions
        for objectId in AnalysisLib.generalObjectPreference:
            AnalysisLib.generalObjectPreference[objectId] /= totalActions

    
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
        if agentId in AnalysisLib.agentIds:
            pullRequestAction = HourlyActionRate(agentId,
                                                 "GITHUB_PULL_REQUEST",
                                                 AnalysisLib.agentHourlyActionRate[agentId])
            pushAction = HourlyActionRate(agentId,
                                          "GITHUB_PUSH",
                                          AnalysisLib.agentHourlyActionRate[agentId])
        else: #This is a new user, no record.
            pullRequestAction = HourlyActionRate(agentId,
                                                 "GITHUB_PULL_REQUEST",
                                                 AnalysisLib.generalHourlyActionRate)
            pushAction = HourlyActionRate(agentId,
                                          "GITHUB_PUSH",
                                          AnalysisLib.generalHourlyActionRate)

        return [pushAction, pullRequestAction]
        

    @staticmethod
    def getAgentObjectPreference(agentId):
        '''
        :return: an ObjectPreference instance
        '''
        if agentId in AnalysisLib.agentIds:
            objectPreference = ObjectPreference(agentId,
                                                AnalysisLib.agentObjectPreference[agentId].keys(),
                                                AnalysisLib.agentObjectPreference[agentId].values())
        else: #This is a new user, no record.
            objectPreference = ObjectPreference(agentId,
                                                AnalysisLib.generalObjectPreference.keys(),
                                                AnalysisLib.generalObjectPreference.values())
        return objectPreference
    
        
    @staticmethod
    def getAgentDependentActions(agentID):
        return None


if __name__ == '__main__':
    analysislib = AnalysisLib()
