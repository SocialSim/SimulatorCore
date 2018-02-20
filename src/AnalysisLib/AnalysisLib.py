from Dependency.ObjectPreference import ObjectPreference
from Dependency.HourlyActionRate import HourlyActionRate
from common.const import *
import numpy as np


class AnalysisLib:
    _instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if AnalysisLib._instance is None:
            AnalysisLib()
        return AnalysisLib._instance

    def __init__(self):
        if AnalysisLib._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            AnalysisLib._instance = self

        self.agentIds = []
        self.objectIds = []
        self.agentObjectPreference = {}
        self.agentHourlyActionRate = {}
        self.agentActionCount = {}
        self.generalObjectPreference = {}
        self.generalHourlyActionRate = np.array([0.0 for i in range(24)])
        with open(DATAPATH + "/test.txt", "r") as file:
            for line in file:
                if not line:
                    break
                else:
                    #Event format: (eventTime,objectId,actorId)
                    event = line.split(",")
                    eventTime = int(event[0])
                    hour = (eventTime / 3600) % 24
                    objectId = int(event[1])
                    agentId = int(event[2])

                    #Update the agentsIds and his records
                    if agentId not in self.agentIds:  #This is a new user.
                        self.agentIds.append(agentId)
                        self.agentActionCount[agentId] = 1

                        #Update the agentHourlyActionRate
                        hourlyActions = np.array([0.0 for i in range(24)])
                        hourlyActions[hour] += 1
                        self.agentHourlyActionRate[agentId] = hourlyActions

                        #Update the agentObjectPreference
                        objectPreference = {objectId: 1.0}
                        self.agentObjectPreference[agentId] = objectPreference
                    else:  #Not a new user.
                        self.agentActionCount[agentId] += 1
                        self.agentHourlyActionRate[agentId][hour] += 1
                        if objectId not in self.agentObjectPreference[
                                agentId]:  #Did not touch this object before
                            self.agentObjectPreference[agentId][objectId] = 1.0
                        else:
                            self.agentObjectPreference[agentId][objectId] += 1
                    #Update the objectIds
                    if objectId not in self.objectIds:
                        self.objectIds.append(objectId)

                    #Update the generalObjectPreference and generalHourlyActionRate
                    if objectId not in self.generalObjectPreference:
                        self.generalObjectPreference[objectId] = 1.0
                    else:
                        self.generalObjectPreference[objectId] += 1
                    self.generalHourlyActionRate[hour] += 1

        #Update the agentHourActionRate and agentObjectPreference
        for agentId in self.agentIds:
            self.agentHourlyActionRate[agentId] /= self.agentActionCount[
                agentId]
            for objectId in self.agentObjectPreference[agentId]:
                self.agentObjectPreference[agentId][
                    objectId] /= self.agentActionCount[agentId]

        #Update the generalObjectPreference and generalHourlyActionRate
        totalActions = sum(self.agentActionCount.values())
        self.generalHourlyActionRate /= totalActions
        for objectId in self.generalObjectPreference:
            self.generalObjectPreference[objectId] /= totalActions

    def getListOfAgentIds(self):
        return self.agentIds

    def getListOfObjIds(self):
        return self.objectIds

    def getAgentIndependentActions(self, agentId):
        return None

    def getAgentHourlyActionRate(self, agentId):
        '''
        :return: a list of HourlyActionRate instances, one for each actionType 
        '''
        if agentId in self.agentIds:
            pullRequestAction = HourlyActionRate(
                agentId, "GITHUB_PULL_REQUEST",
                self.agentHourlyActionRate[agentId])
            pushAction = HourlyActionRate(agentId, "GITHUB_PUSH",
                                          self.agentHourlyActionRate[agentId])
        else:  #This is a new user, no record.
            pullRequestAction = HourlyActionRate(agentId, "GITHUB_PULL_REQUEST",
                                                 self.generalHourlyActionRate)
            pushAction = HourlyActionRate(agentId, "GITHUB_PUSH",
                                          self.generalHourlyActionRate)

        return [pushAction, pullRequestAction]

    def getAgentObjectPreference(self, agentId):
        '''
        :return: an ObjectPreference instance
        '''
        if agentId in self.agentIds:
            objectPreference = ObjectPreference(
                agentId, self.agentObjectPreference[agentId].keys(),
                self.agentObjectPreference[agentId].values())
        else:  #This is a new user, no record.
            objectPreference = ObjectPreference(
                agentId, self.generalObjectPreference.keys(),
                self.generalObjectPreference.values())
        return objectPreference

    def getAgentDependentActions(self, agentID):
        return None


if __name__ == '__main__':
    analysislib = AnalysisLib()
