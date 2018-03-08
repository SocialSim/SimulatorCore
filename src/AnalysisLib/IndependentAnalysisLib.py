from common.const import *
import numpy as np
from collections import deque
import copy
import time
import json
import pickle
import common.analysisArgParser as argParser

from Dependency.ObjectPreference import ObjectPreference
from Dependency.HourlyActionRate import HourlyActionRate


class IndependentAnalysisLib:
    _instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if IndependentAnalysisLib._instance is None:
            IndependentAnalysisLib()
        return IndependentAnalysisLib._instance

    def __init__(self):
        if IndependentAnalysisLib._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            IndependentAnalysisLib._instance = self

        self.activityThreshold = 10 #Users with activities over this threshold will be set as active users.
        self.userIds = []
        self.objectIds = []
        self.eventTypes = ["CommitCommentEvent", "CreateEvent", "DeleteEvent", "ForkEvent", "IssueCommentEvent",
                           "IssuesEvent", "PullRequestEvent", "PushEvent", "WatchEvent", "PublicEvent",
                           "MemberEvent", "GollumEvent", "ReleaseEvent", "PullRequestReviewCommentEvent"]
        self.userObjectPreference = {}
        self.userHourlyActionRate = {} #Should only count the independent actions, specific to event types.
        self.userTotalActionCount = {}
        self.generalTypeActionCount = {} # The general count of actions belonging to each type.
        self.generalObjectPreference = {}
        self.generalHourlyActionRate = self.initializeHourlyDistributions()


        #The first pass, we determine user hourly action rate
        self.firstPass()

        #Extract the general hourlyActionRate and objectPreference
        self.summarizeGeneralDistribtions()

        #Update the userHourActionRate and userObjectPreference
        self.summarizeUserDistributions()


    def firstPass(self):
        '''
        The first pass, we determine the initial dependencies, and user hourly action rate
        Will clean the dependencies, and do a seconde pass to update the independent actions
        :return:
        '''
        with open(DATAPATH + argParser.sargs.dataset, "r") as file:
            for line in file:
                if not line:
                    break
                else:
                    line = line.strip('\n')
                    eventTime, hour, objectId, userId, eventType = self.eventSplit(line)

                    #Update the objectIds
                    if objectId not in self.objectIds:
                        self.objectIds.append(objectId)

                    #Update the userId and his records
                    if userId not in self.userIds:  #This is a new user.
                        self.userIds.append(userId)
                        self.userTotalActionCount[userId] = 1
                        #Update the userHourlyActionRate
                        self.updateUserHourlyActionRate(userId, hour, eventType, "new")
                        #Update the userObjectPreference
                        self.updateUserObjectPreference(userId, objectId, "new")

                    else:  #Not a new user.
                        self.userTotalActionCount[userId] += 1
                        #Update the userHourlyActionRate
                        self.updateUserHourlyActionRate(userId, hour, eventType, "old")
                        #Update the userObjectPreference
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
        eventTime = int(event[0])
        hour = int((eventTime / 3600) % 24)
        objectId = event[1]
        userId = event[2]
        eventType = event[3]
        return eventTime, hour, objectId, userId, eventType

    def initializeHourlyDistributions(self):
        '''
        Initialize the hourly action distribution
        :return:
        '''
        initialHourlyActionRate = {}
        for eventType in self.eventTypes:
            initialHourlyActionRate[eventType] = np.array([0.0 for i in range(24)])
        return copy.deepcopy(initialHourlyActionRate)

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
        self.generalHourlyActionRate[eventType][hour] += 1

    def summarizeGeneralDistribtions(self):
        '''
        Compute the general distributions based on the general statistics.
        :return:
        '''
        totalActions = sum(self.userTotalActionCount.values())
        for eventType in self.eventTypes:
            self.generalTypeActionCount[eventType] = sum(self.generalHourlyActionRate[eventType])
            if self.generalTypeActionCount[eventType] > 0:
                self.generalHourlyActionRate[eventType] /= self.generalTypeActionCount[eventType]
        for objectId in self.generalObjectPreference:
            self.generalObjectPreference[objectId] /= totalActions

    def updateUserHourlyActionRate(self, userId, hour, eventType, userType):
        '''
        In the first pass, regard all the events as independent, and add them to hourly distribution.
        :param userId:
        :param hour:
        :param userType:
        :return:
        '''
        if userType == "new":
            self.userHourlyActionRate[userId] = self.initializeHourlyDistributions()

        self.userHourlyActionRate[userId][eventType][hour] += 1

    def updateUserObjectPreference(self, userId, objectId, userType):
        '''
        In the first pass, update the user object preference.
        :param userId:
        :param objectId:
        :param userType:
        :return:
        '''
        if userType == "new":
            objectPreference = {objectId: 1.0}
            self.userObjectPreference[userId] = objectPreference
        else:
            if objectId not in self.userObjectPreference[userId]:  # Did not touch this object before
                self.userObjectPreference[userId][objectId] = 1.0
            else:
                self.userObjectPreference[userId][objectId] += 1

    def summarizeUserDistributions(self):
        '''
        Summarize the user hourlyActionRate and objectPreference
        :return:
        '''
        for userId in self.userIds:
            for eventType in self.eventTypes:
                userTypeEventCount = self.userTypeEventCount(userId, eventType)
                if userTypeEventCount > 0:
                    self.userHourlyActionRate[userId][eventType] /= userTypeEventCount
            for objectId in self.userObjectPreference[userId]:
                self.userObjectPreference[userId][
                    objectId] /= self.userTotalActionCount[userId]

    def isActiveUser(self, userId):
        '''
        :param userId:
        :return: Return if this user is an active user, cause we only the influence of active users.
        '''
        return self.userTotalActionCount[userId] > self.activityThreshold

    def hour(self, eventTime):
        return int((eventTime / 3600) % 24)

    def userTypeEventCount(self, userId, eventType):
        return sum(self.userHourlyActionRate[userId][eventType])

    def getUserIds(self):
        return self.userIds

    def getObjectIds(self):
        return self.objectIds

    def getEventTypes(self):
        return self.eventTypes

    def getUserIndependentActions(self, userId):
        return None

    def getUserHourlyActionRate(self, userId):
        '''
        :return: a list of HourlyActionRate instances, one for each actionType
        '''
        userHourlyActionRate = []
        if userId in self.userIds:
            for eventType in self.eventTypes:
                eventTypeHourlyActionRate = HourlyActionRate(
                    userId, self.userTypeEventCount(userId, eventType), eventType,
                    self.userHourlyActionRate[userId][eventType]
                )
                userHourlyActionRate.append(eventTypeHourlyActionRate)
        else:  #This is a new user, no record.
            for eventType in self.eventTypes:
                eventTypeHourlyActionRate = HourlyActionRate(
                    userId, self.generalTypeActionCount[eventType], eventType,
                    self.generalHourlyActionRate[eventType]
                )
                userHourlyActionRate.append(eventTypeHourlyActionRate)

        return userHourlyActionRate

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

    def storeStatistics(self):
        self.checkStatFolder()
        self.storeUserID()
        self.storeObjID()
        self.storeUserActionRate()
        self.storeUserObjectPreference()

    def checkStatFolder(self):
        if not os.path.exists(STAT_PATH):
            os.makedirs(STAT_PATH)

    def storeUserID(self):
        pickle.dump(self.userIds, open(USER_ID_FILE,'w'))

    def storeObjID(self):
        pickle.dump(self.objectIds, open(OBJ_ID_FILE,'w'))

    def storeUserActionRate(self):
        allActionRate = dict()
        for userId in self.userIds:
            actionRate = self.getUserHourlyActionRate(userId)
            allActionRate[userId] = actionRate

        newUserActionRate = self.getUserHourlyActionRate(-1)
        allActionRate[-1] = newUserActionRate

        pickle.dump(allActionRate, open(USER_ACTION_RATE_FILE,'w'))

        # favorite_color = pickle.load( open( USER_ACTION_RATE_FILE, "rb" ) )

    def storeUserObjectPreference(self):
        allObjectPreference = dict()
        for userId in self.userIds:
            objectPreference = self.getUserObjectPreference(userId)
            allObjectPreference[userId] = objectPreference

        newUserObjectPreference = self.getUserObjectPreference(-1)
        allObjectPreference[-1] = newUserObjectPreference

        pickle.dump(allObjectPreference, open(OBJECT_PREFERENCE_FILE,'w'))


if __name__ == '__main__':
    start = time.time()
    independentAnalysisLib = IndependentAnalysisLib()
    end = time.time()
    print("Analyze time: %f"%(end-start))
    # for userId in IndependentAnalysisLib.userIds:
    #     if IndependentAnalysisLib.getUserDependency(userId).userDependency:
    #         print("User Id: %s"%userId, "number of actions: %d"%IndependentAnalysisLib.userTotalActionCount[userId],
    #               "dependencies: ", IndependentAnalysisLib.getUserDependency(userId).userDependency)
        # print(IndependentAnalysisLib.userTotalActionCount[userId])
        # print(IndependentAnalysisLib.userHourlyActionRate[userId])
    for eventType in independentAnalysisLib.eventTypes:
        print(eventType, independentAnalysisLib.generalTypeActionCount[eventType])
        # print(eventType, IndependentAnalysisLib.generalHourlyActionRate[eventType])