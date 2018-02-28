from common.const import *
import numpy as np
from collections import deque

from Dependency.ObjectPreference import ObjectPreference
from Dependency.HourlyActionRate import HourlyActionRate
from Dependency.UserDependency import UserDependency


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

        self.dependencyTimeLength = 50 #Initially set the dependency window size as one hour
        self.dependencyWindow = deque() #Use a queue to represent the events within the dependency time window
        self.userIds = []
        self.objectIds = []
        self.userObjectPreference = {}
        self.userHourlyActionRate = {}
        self.userActionCount = {}
        self.userDependencies = {}
        self.generalObjectPreference = {}
        self.generalHourlyActionRate = np.array([0.0 for i in range(24)])
        with open(DATAPATH + "/test.txt", "r") as file:
            for line in file:
                if not line:
                    break
                else:
                    #Event format: (eventTime, objectId, userId)
                    event = line.split(",")
                    eventTime = int(event[0])
                    hour = int((eventTime / 3600) % 24)
                    objectId = int(event[1])
                    userId = int(event[2])

                    #update the dependencyWindow
                    self.updateDependencyWindow(eventTime)

                    #Update the userId and his records
                    if userId not in self.userIds:  #This is a new user.
                        self.userIds.append(userId)
                        self.userActionCount[userId] = 1

                        #Update the userHourlyActionRate
                        hourlyActions = np.array([0.0 for i in range(24)])
                        hourlyActions[hour] += 1
                        self.userHourlyActionRate[userId] = hourlyActions

                        #Update the userObjectPreference
                        objectPreference = {objectId: 1.0}
                        self.userObjectPreference[userId] = objectPreference

                        #Update the userDependencies
                        if self.dependencyWindow: #There is a need to update.
                            dependency = {}
                            for event in self.dependencyWindow:
                                dependentUserId = event[2]
                                if dependentUserId == userId:
                                    continue
                                dependency[dependentUserId] = 1.0
                            self.userDependencies[userId] = dependency
                        else:
                            self.userDependencies[userId] = {}

                    else:  #Not a new user.
                        self.userActionCount[userId] += 1
                        self.userHourlyActionRate[userId][hour] += 1

                        #Update the userObjectPreference
                        if objectId not in self.userObjectPreference[
                                userId]:  #Did not touch this object before
                            self.userObjectPreference[userId][objectId] = 1.0
                        else:
                            self.userObjectPreference[userId][objectId] += 1

                        # Update the userDependencies
                        if self.dependencyWindow:
                            dependency = {} #Avoid the mulitple occurence for one singe user in the dependency window
                            for event in self.dependencyWindow:
                                dependentUserId = event[2]
                                if dependentUserId == userId:
                                    continue
                                dependency[dependentUserId] = 1.0
                            for dependentUserId in dependency:
                                if dependentUserId not in self.userDependencies[userId]:
                                    self.userDependencies[userId][dependentUserId] = 1.0
                                else:
                                    self.userDependencies[userId][dependentUserId] += 1
                    #Update the objectIds
                    if objectId not in self.objectIds:
                        self.objectIds.append(objectId)

                    #Update the generalObjectPreference and generalHourlyActionRate
                    if objectId not in self.generalObjectPreference:
                        self.generalObjectPreference[objectId] = 1.0
                    else:
                        self.generalObjectPreference[objectId] += 1
                    self.generalHourlyActionRate[hour] += 1

                    # Append this event to the dependnecy window
                    self.dependencyWindow.append([eventTime, objectId, userId])

        #Update the userHourActionRate and userObjectPreference
        for userId in self.userIds:
            self.userHourlyActionRate[userId] /= self.userActionCount[
                userId]
            for objectId in self.userObjectPreference[userId]:
                self.userObjectPreference[userId][
                    objectId] /= self.userActionCount[userId]
            for dependentUserId in self.userDependencies[userId]:
                self.userDependencies[userId][dependentUserId] /= self.userActionCount[userId]

        #Update the generalObjectPreference and generalHourlyActionRate
        totalActions = sum(self.userActionCount.values())
        self.generalHourlyActionRate /= totalActions
        for objectId in self.generalObjectPreference:
            self.generalObjectPreference[objectId] /= totalActions


    def updateDependencyWindow(self, currentEventTime):
        '''
        This function update the events in the dependency window according to the current event time
        It will pop the events out of the window.
        :param currentEventTime:
        :return: no return
        '''
        lowerTimeLimit = currentEventTime - self.dependencyTimeLength
        while True:
            if self.dependencyWindow: # Dependency window is not empty
                tailEvent = self.dependencyWindow.popleft() #(eventTime, objID, userID)
                if tailEvent[0] >= lowerTimeLimit:
                    self.dependencyWindow.appendleft(tailEvent)
                    return
                else:
                    continue
            else:
                break


    def getUserIds(self):
        return self.userIds

    def getObjectIds(self):
        return self.objectIds

    def getUserIndependentActions(self, userId):
        return None

    def getUserHourlyActionRate(self, userId):
        '''
        :return: a list of HourlyActionRate instances, one for each actionType 
        '''
        if userId in self.userIds:
            pullRequestAction = HourlyActionRate(
                userId, "GITHUB_PULL_REQUEST",
                self.userHourlyActionRate[userId])
            pushAction = HourlyActionRate(userId, "GITHUB_PUSH",
                                          self.userHourlyActionRate[userId])
        else:  #This is a new user, no record.
            pullRequestAction = HourlyActionRate(userId, "GITHUB_PULL_REQUEST",
                                                 self.generalHourlyActionRate)
            pushAction = HourlyActionRate(userId, "GITHUB_PUSH",
                                          self.generalHourlyActionRate)

        return [pushAction, pullRequestAction]

    def getUserObjectPreference(self, userId):
        '''
        :return: an ObjectPreference instance
        '''
        if userId in self.userIds:
            objectPreference = ObjectPreference(
                userId, list(self.userObjectPreference[userId].keys()),
                list(self.userObjectPreference[userId].values()))
        else:  #This is a new user, no record.
            objectPreference = ObjectPreference(
                userId, self.generalObjectPreference.keys(),
                self.generalObjectPreference.values())
        return objectPreference

    def getUserDependency(self, userId):
        '''
        Return: the dependency this user has from the hitory.
        :param userId:
        :return: A dictionary of his dependent relationship.
        '''
        if userId in self.userIds:
            userDependency = UserDependency(
                userId, list(self.userDependencies[userId].keys()),
                list(self.userDependencies[userId].values())
            )
        else:
            userDependency = UserDependency(
                userId, [], [])
        return userDependency

    def getUserDependentActions(self, userID):
        return None


if __name__ == '__main__':
    analysislib = AnalysisLib()
    for userId in analysislib.userIds:
        print(analysislib.userDependencies[userId])
