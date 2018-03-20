from common.const import *
import numpy as np
from collections import deque
import copy
import time
import json
import sys
import pickle
import common.analysisArgParser as argParser
import matplotlib.pyplot as plt

from Dependency.ObjectPreference import ObjectPreference
from Dependency.HourlyActionRate import HourlyActionRate
from Dependency.TypeDistribution import TypeDistribution
from common.simulationTime import SimulationTime


class IndependentAnalysisLib(object):
    _instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if IndependentAnalysisLib._instance is None:
            IndependentAnalysisLib()
        return IndependentAnalysisLib._instance

    def __init__(self , fileName = None):
        if IndependentAnalysisLib._instance is not None:
            raise Exception("IndependentAnalysisLib class is a singleton!")
        else:
            IndependentAnalysisLib._instance = self

        if fileName:
            self.fileName = DATAPATH + fileName
        else:
            self.fileName = DATAPATH + argParser.sargs.dataset

        self.activityThreshold = 50 #Users with activities over this threshold will be set as active users.
        self.userIds = {} #Store the user IDs, and their number of total actions.
        self.objectIds = {} #Store the obj IDs, and their number of total actions.
        self.eventTypes = {"CommitCommentEvent": 0, "CreateEvent": 1, "DeleteEvent": 2, "ForkEvent": 3,
                           "IssueCommentEvent": 4, "IssuesEvent": 5, "PullRequestEvent": 6, "PushEvent": 7,
                           "WatchEvent": 8, "PublicEvent": 9, "MemberEvent": 10, "GollumEvent": 11,
                           "ReleaseEvent": 12, "PullRequestReviewCommentEvent": 13}

        self.userObjectPreference = {}
        self.userHourlyActionRate = {} #Should only count the independent actions, specific to event types.
        self.userTypeDistribution = {}

        self.generalTotalActionCount = 0
        self.generalTypeDistribution = np.array([0.0 for i in range(len(self.eventTypes))])
        self.generalObjectPreference = {}
        self.generalHourlyActionRate = np.array([0.0 for i in range(24)])


        #The first pass, we determine user hourly action rate
        self.firstPass()

        #The second pass, calculate the hourlyActionRate and objectPreference
        self.secondPass()

        #Extract the general hourlyActionRate and objectPreference
        self.summarizeGeneralDistribtions()

        #Update the userHourActionRate and userObjectPreference
        self.summarizeUserDistributions()

        #Store the calculated parameters
        self.storeStatistics()


    def firstPass(self):
        '''
        The first pass, we will only count the userIds, objIds, user activity levels.
        :return:
        '''
        with open(self.fileName, "r") as file:
            for line in file:
                if not line:
                    break
                else:
                    line = line.strip('\n')
                    eventTime, hour, objectId, userId, eventType = self.eventSplit(line)

                    #Update the objectIds and the event number
                    if objectId not in self.objectIds:
                        self.objectIds[objectId] = 1.0
                    else:
                        self.objectIds[objectId] += 1

                    #Update the userId and the action number
                    if userId not in self.userIds:
                        self.userIds[userId] = 1.0
                    else:  #Not a new user.
                        self.userIds[userId] += 1

                    self.generalTotalActionCount += 1

    def secondPass(self):
        '''
        In this pass, we will compute the hourly action rate and object preference.

        Note: We will not compute hourly action rate for inactive users.
        :return:
        '''
        with open(self.fileName, "r") as file:
            for line in file:
                if not line:
                    break
                else:
                    line = line.strip('\n')
                    eventTime, hour, objectId, userId, eventType = self.eventSplit(line)

                    #Update the user hourly action rate and type distribution for active users
                    if self.userIds[userId] > self.activityThreshold:

                        if userId not in self.userHourlyActionRate:
                            self.updateUserHourlyActionRate(userId, hour, "new")
                        else:
                            self.updateUserHourlyActionRate(userId, hour, "old")

                        if userId not in self.userTypeDistribution:
                            self.updateUserTypeDistribution(userId, eventType, "new")
                        else:
                            self.updateUserTypeDistribution(userId, eventType, "old")

                    #Upadate the object preference for all users
                    if userId not in self.userObjectPreference:
                        self.updateUserObjectPreference(userId, objectId, "new")
                    else:
                        self.updateUserObjectPreference(userId, objectId, "old")

                    #Update the general hourlyActionRate and objectPreference
                    self.updateGeneralDistributions(objectId, hour, eventType)

    def eventSplit(self, line):
        '''
        Given a line of input, extract the attributes.
        :param line: A line of input with format #Event format: (eventTime, objectId, userId)
        :return:
        '''
        event = line.split(" ")
        eventTime = event[0]
        hour = SimulationTime.getHourFromIso(eventTime)
        objectId = event[1]
        userId = event[2]
        eventType = event[3]
        return eventTime, hour, objectId, userId, eventType

    def updateGeneralDistributions(self, objectId, hour, eventType):
        '''
        Update the general HourlyActionRate and ObjectPreference
        :param objId:
        :return:
        '''
        if objectId not in self.generalObjectPreference:
            self.generalObjectPreference[objectId] = 1.0
        else:
            self.generalObjectPreference[objectId] += 1

        self.generalHourlyActionRate[hour] += 1

        typeIndex = self.eventTypes[eventType]
        self.generalTypeDistribution[typeIndex] += 1


    def updateUserHourlyActionRate(self, userId, hour, userType):
        '''
        Upate the hourly action distribution of each user.
        :param userId:
        :param hour:
        :param userType:
        :return:
        '''
        if userType == "new":
            self.userHourlyActionRate[userId] = np.array([0.0 for i in range(24)])

        self.userHourlyActionRate[userId][hour] += 1

    def updateUserTypeDistribution(self, userId, eventType, userType):
        '''
        Update the event type distribution of each user.
        :param userId:
        :param eventType:
        :param userType:
        :return:
        '''
        if userType == "new":
            self.userTypeDistribution[userId] = np.array([0.0 for i in range(len(self.eventTypes))])

        typeIndex = self.eventTypes[eventType]
        self.userTypeDistribution[userId][typeIndex] += 1

    def updateUserObjectPreference(self, userId, objectId, userType):
        '''
        In the first pass, update the user object preference.
        :param userId:
        :param objectId:
        :param userType:
        :return:
        '''
        if userType == "new":
            self.userObjectPreference[userId] = {objectId: 1.0}
        else:
            if objectId not in self.userObjectPreference[userId]:  # Did not touch this object before
                self.userObjectPreference[userId][objectId] = 1.0
            else:
                self.userObjectPreference[userId][objectId] += 1

    def summarizeGeneralDistribtions(self):
        '''
        Compute the general distributions based on the general statistics.
        :return:
        '''

        self.generalTypeDistribution /= self.generalTotalActionCount

        for objectId in self.generalObjectPreference:
            self.generalObjectPreference[objectId] /= self.generalTotalActionCount

        for hour in range(24):
            self.generalHourlyActionRate[hour] /= self.generalTotalActionCount

    def summarizeUserDistributions(self):
        '''
        Summarize the user hourlyActionRate and objectPreference
        :return:
        '''
        for userId in self.userHourlyActionRate:
            self.userHourlyActionRate[userId] /= self.userIds[userId]

        for userId in self.userTypeDistribution:
            self.userTypeDistribution[userId] /= self.userIds[userId]

        for userId in self.userObjectPreference:
            for objectId in self.userObjectPreference[userId]:
                self.userObjectPreference[userId][objectId] /= self.userIds[userId]

    def isActiveUser(self, userId):
        '''
        :param userId:
        :return: Return if this user is an active user, cause we only the influence of active users.
        '''
        return self.userIds[userId] > self.activityThreshold

    def getUserIds(self):
        return self.userIds

    def getObjectIds(self):
        return self.objectIds

    def getEventTypes(self):
        return self.eventTypes.keys()

    def getUserIndependentActions(self, userId):
        return None

    def getUserHourlyActionRate(self, userId):
        '''
        :return: a list of HourlyActionRate instances, one for each actionType;

        Note: Users with less than 5 records will user the general distribution.
        '''
        if userId in self.userHourlyActionRate:
            userHourlyActionRate = HourlyActionRate(userId, self.userIds[userId]/31,
                                                    self.userHourlyActionRate[userId])
        else:  #This is a new user, no record; or he has too few records.
            if userId in self.userIds:
                userHourlyActionRate = HourlyActionRate(userId, self.userIds[userId]/31,
                                                    self.generalHourlyActionRate)
            else:
                averageDailyActivityLevel = float(self.generalTotalActionCount) / (len(self.userIds.keys()) * 31)
                userHourlyActionRate = HourlyActionRate(userId, averageDailyActivityLevel,
                                                        self.generalHourlyActionRate)
        return userHourlyActionRate

    def getUserObjectPreference(self, userId):
        '''
        :return: an ObjectPreference instance

        Note: Different from hourlyRate, each user with record will have a object preference.
        '''
        if userId in self.userObjectPreference:
            objectPreference = ObjectPreference(
                userId, list(self.userObjectPreference[userId].keys()),
                list(self.userObjectPreference[userId].values()))
        else:  #This is a new user, no record.
            objectPreference = ObjectPreference(
                userId, self.generalObjectPreference.keys(),
                self.generalObjectPreference.values())

        return objectPreference

    def getUserTypeDistribution(self, userId):
        '''
        Get the type action distribution of the given user.
        :param userId:
        :return:
        '''
        if userId in self.userTypeDistribution:
            typeDistribution = TypeDistribution(userId, self.userTypeDistribution[userId])
        else:
            typeDistribution = TypeDistribution(userId, self.generalTypeDistribution)

        return typeDistribution

    def getUserDependentActions(self, userID):
        return None

    def storeStatistics(self):
        self.checkStatFolder()
        self.storeUserID()
        self.storeObjID()
        self.storeUserActionRate()
        self.storeUserObjectPreference()
        self.storeUserTypeDistribution()

    def checkStatFolder(self):
        if not os.path.exists(STAT_PATH):
            os.makedirs(STAT_PATH)

    def storeUserID(self):
        pickle.dump(self.userIds, open(USER_ID_FILE,'w'))

    def storeObjID(self):
        pickle.dump(self.objectIds, open(OBJ_ID_FILE,'w'))

    def storeUserActionRate(self):
        allActionRate = dict()
        for userId in self.userHourlyActionRate:
            actionRate = self.getUserHourlyActionRate(userId)
            allActionRate[userId] = actionRate

        newUserActionRate = self.getUserHourlyActionRate(-1)
        allActionRate[-1] = newUserActionRate

        pickle.dump(allActionRate, open(USER_ACTION_RATE_FILE,'w'))

    def storeUserObjectPreference(self):
        allObjectPreference = dict()
        for userId in self.userObjectPreference:
            objectPreference = self.getUserObjectPreference(userId)
            allObjectPreference[userId] = objectPreference

        newUserObjectPreference = self.getUserObjectPreference(-1)
        allObjectPreference[-1] = newUserObjectPreference

        pickle.dump(allObjectPreference, open(OBJECT_PREFERENCE_FILE,'w'))

    def storeUserTypeDistribution(self):
        allTypeDistribution = dict()
        for userId in self.userTypeDistribution:
            typeDistritbuion = self.getUserTypeDistribution(userId)
            allTypeDistribution[userId] = typeDistritbuion

        newUserTypeDistribution = self.getUserTypeDistribution(-1)
        allTypeDistribution[-1] = newUserTypeDistribution

        pickle.dump(allTypeDistribution, open(TYPE_DISTRIBUTION_FILE, 'w'))

    def getMostActiveUser(self):
        '''
        Get the id of most active user.
        :return:
        '''
        return max(self.userIds, key=self.userIds.get)

    def plotGeneralHourlyDistribution(self):
        '''
        Function for plot the general general hourly activity distribution.
        :return:
        '''
        x = np.arange(0, 24)
        y = self.generalHourlyActionRate
        fig = plt.bar(x, y)
        plt.xlabel("Hour")
        # plt.xticks(x, x, rotation=-90)
        plt.ylabel("Proportion")
        plt.title("General hourly action ditribution")
        plt.show()

    def plotGeneralTypeDistribution(self):
        '''
        Function for plot the general type distribution.
        :return:
        '''
        x = self.eventTypes
        y = self.generalTypeDistribution
        fig = plt.bar(x, y)
        plt.tight_layout()
        plt.xlabel("Event Type")
        plt.xticks(x, x, rotation=-90)
        plt.ylabel("Proportion")
        plt.title("General action type distribution")
        plt.show()

    def plotUserHourlyDistribution(self, userId):
        '''
        Plot the hourly activity distribution for given user.
        :return:
        '''
        x = np.arange(0, 24)
        y = self.userHourlyActionRate[userId]
        plt.bar(x, y)
        plt.xlabel("Hour")
        # plt.xticks(x, x, rotation=-90)
        plt.ylabel("Proportion")
        plt.title("Hourly action distribution of user: %s"%userId)
        plt.show()

    def plotUserTypeDistribution(self, userId):
        '''
        Plot the type activity distribution for given user.
        :param userId:
        :return:
        '''
        x = self.eventTypes.keys()
        y = self.userTypeDistribution[userId] * self.userIds[userId]
        plt.bar(x, y)
        plt.tight_layout()
        plt.xlabel("Event Type")
        plt.xticks(x, x, rotation=-90)
        plt.ylabel("Count")
        plt.title("Action type distribution for user: %s"%userId)
        plt.show()


if __name__ == '__main__':
    start = time.time()
    fileName = sys.argv[1]
    independentAnalysisLib = IndependentAnalysisLib(fileName)
    end = time.time()
    print("Analyze time: %f"%(end-start))

    totalActions = 0
    totalRepos = 0
    for user in independentAnalysisLib.userIds:
        if independentAnalysisLib.userIds[user] > 50:
            totalActions += independentAnalysisLib.userIds[user]
            totalRepos += len(independentAnalysisLib.userObjectPreference[user].keys())

    print("Number of active users: %d"%len(independentAnalysisLib.userHourlyActionRate.keys()))
    print("Average daily activity level: %f"%(totalActions /
                                              len(independentAnalysisLib.userHourlyActionRate.keys())))
    print("Average number of repos: %d"%(totalRepos /len(independentAnalysisLib.userHourlyActionRate.keys()) ))

    # # mostActiveuser = independentAnalysisLib.getMostActiveUser()
    # print("Number of users: %d"%len(independentAnalysisLib.userIds.keys()))
    # print("Number of objects: %d"%len(independentAnalysisLib.objectIds.keys()))
    # print(independentAnalysisLib.generalHourlyActionRate)
    # mostActiveuser = "mGzHxRUb6V36nyFJgEXPeQ"
    # mostActiveuser = "YyAXRlZYVhUlbHCublQjzg"
    # independentAnalysisLib.plotUserHourlyDistribution(mostActiveuser)
    # independentAnalysisLib.plotUserTypeDistribution(mostActiveuser)
