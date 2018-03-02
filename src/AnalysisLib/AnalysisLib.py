from common.const import *
import numpy as np
import time

from Dependency.ObjectPreference import ObjectPreference
from Dependency.HourlyActionRate import HourlyActionRate

from Database.DatabaseInterface import DatabaseInterface


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

        self.databaseConnection = DatabaseInterface()
    
        self.userIds = []
        self.objectIds = []
        self.userObjectPreference = {}
        self.userHourlyActionRate = {}
        self.userActionCount = {}
        self.generalObjectPreference = {}
        self.generalHourlyActionRate = np.array([0.0 for i in range(24)])
        for line in self.databaseConnection.getBaseEventStream("PushEvent"):
            eventTime = int(time.mktime(line["timestamp"].timetuple()))
            hour = int((eventTime / 3600) % 24)
            objectId = line["objectId"]
            userId = line["userId"]

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
            else:  #Not a new user.
                self.userActionCount[userId] += 1
                self.userHourlyActionRate[userId][hour] += 1
                if objectId not in self.userObjectPreference[
                        userId]:  #Did not touch this object before
                    self.userObjectPreference[userId][objectId] = 1.0
                else:
                    self.userObjectPreference[userId][objectId] += 1
            #Update the objectIds
            if objectId not in self.objectIds:
                self.objectIds.append(objectId)

            #Update the generalObjectPreference and generalHourlyActionRate
            if objectId not in self.generalObjectPreference:
                self.generalObjectPreference[objectId] = 1.0
            else:
                self.generalObjectPreference[objectId] += 1
            self.generalHourlyActionRate[hour] += 1

        #Update the userHourActionRate and userObjectPreference
        for userId in self.userIds:
            self.userHourlyActionRate[userId] /= self.userActionCount[
                userId]
            for objectId in self.userObjectPreference[userId]:
                self.userObjectPreference[userId][
                    objectId] /= self.userActionCount[userId]

        #Update the generalObjectPreference and generalHourlyActionRate
        totalActions = sum(self.userActionCount.values())
        self.generalHourlyActionRate /= totalActions
        for objectId in self.generalObjectPreference:
            self.generalObjectPreference[objectId] /= totalActions

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

    def getUserDependentActions(self, userID):
        return None


if __name__ == '__main__':
    analysislib = AnalysisLib()
