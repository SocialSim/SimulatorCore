from common.const import *
import numpy as np
from collections import deque
import copy
import time
import json
import common.analysisArgParser as argParser

from Dependency.ObjectPreference import ObjectPreference
from Dependency.HourlyActionRate import HourlyActionRate
from AnalysisLib import AnalysisLib

# FILE_NAME = "/Users/liushengzhong/Desktop/Code/Python/SimulatorCore/data/event_2015-01-18_24.txt"
# FILE_NAME = "/Users/liushengzhong/Desktop/Code/Python/SimulatorCore/data/100-compressed_event_2015-01-01.txt"

class IndependentAnalysisLib(AnalysisLib):

    def __init__(self):
        AnalysisLib.__init__(self)

        self.activityThreshold = 10 #Users with activities over this threshold will be set as active users.
        # self.userIds = {} #Store the user IDs, and their number of total actions.
        # self.objectIds = {} #Store the obj IDs, and their number of total actions.
        self.eventTypes = ["CommitCommentEvent", "CreateEvent", "DeleteEvent", "ForkEvent", "IssueCommentEvent",
                           "IssuesEvent", "PullRequestEvent", "PushEvent", "WatchEvent", "PublicEvent",
                           "MemberEvent", "GollumEvent", "ReleaseEvent", "PullRequestReviewCommentEvent"]
        # self.userObjectPreference = {}
        # self.userHourlyActionRate = {} #Should only count the independent actions, specific to event types.
        self.generalTypeActionCount = {} # The general count of actions belonging to each type.
        self.generalTypeActionRatio = {}
        self.generalObjectPreference = {}
        self.generalHourlyActionRate = self.initializeHourlyDistributions()


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
        with open(DATAPATH + argParser.sargs.dataset, "r") as file:
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

    def secondPass(self):
        '''
        In this pass, we will compute the hourly action rate and object preference.

        Note: We will not compute hourly action rate for inactive users.
        :return:
        '''
        with open(DATAPATH + argParser.sargs.dataset, "r") as file:
            for line in file:
                if not line:
                    break
                else:
                    line = line.strip('\n')
                    eventTime, hour, objectId, userId, eventType = self.eventSplit(line)

                    #Update the user hourly action rate for active users
                    if self.userIds[userId] > self.activityThreshold:
                        if userId not in self.userHourlyActionRate:
                            self.updateUserHourlyActionRate(userId, hour, eventType, "new")
                        else:
                            self.updateUserHourlyActionRate(userId, hour, eventType, "old")

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

    def summarizeGeneralDistribtions(self):
        '''
        Compute the general distributions based on the general statistics.
        :return:
        '''
        totalActions = sum(self.userIds.values())

        for eventType in self.eventTypes:
            self.generalTypeActionCount[eventType] = sum(self.generalHourlyActionRate[eventType])
            self.generalTypeActionRatio[eventType] = self.generalTypeActionCount[eventType] / totalActions
            if self.generalTypeActionCount[eventType] > 0:
                self.generalHourlyActionRate[eventType] /= self.generalTypeActionCount[eventType]

        for objectId in self.generalObjectPreference:
            self.generalObjectPreference[objectId] /= totalActions

    def summarizeUserDistributions(self):
        '''
        Summarize the user hourlyActionRate and objectPreference
        :return:
        '''
        for userId in self.userHourlyActionRate:
            for eventType in self.eventTypes:
                userTypeEventCount = self.userTypeEventCount(userId, eventType)
                if userTypeEventCount > 0:
                    self.userHourlyActionRate[userId][eventType] /= userTypeEventCount

        for userId in self.userObjectPreference:
            for objectId in self.userObjectPreference[userId]:
                self.userObjectPreference[userId][objectId] /= self.userIds[userId]

    def isActiveUser(self, userId):
        '''
        :param userId:
        :return: Return if this user is an active user, cause we only the influence of active users.
        '''
        return self.userIds[userId] > self.activityThreshold

    def hour(self, eventTime):
        return int((eventTime / 3600) % 24)

    def userTypeEventCount(self, userId, eventType):
        return sum(self.userHourlyActionRate[userId][eventType])

    def getEventTypes(self):
        return self.eventTypes

    def getUserIndependentActions(self, userId):
        return None

    def getUserHourlyActionRate(self, userId):
        '''
        :return: a list of HourlyActionRate instances, one for each actionType;

        Note: Users with less than 5 records will user the general distribution.
        '''
        userHourlyActionRate = []
        if userId in self.userHourlyActionRate:
            for eventType in self.eventTypes:
                eventTypeHourlyActionRate = HourlyActionRate(
                    userId, self.userTypeEventCount(userId, eventType), eventType,
                    self.userHourlyActionRate[userId][eventType]
                )
                userHourlyActionRate.append(eventTypeHourlyActionRate)
        else:  #This is a new user, no record; or he has too few records.
            for eventType in self.eventTypes:
                if userId in self.userIds:
                    typeActionCount = self.userIds[userId] * self.generalTypeActionRatio[eventType]
                else:
                    averageTypeActionCount = self.generalTypeActionCount[eventType] / len(self.userIds)
                    typeActionCount = averageTypeActionCount
                    eventTypeHourlyActionRate = HourlyActionRate(
                    userId, typeActionCount, eventType,
                    self.generalHourlyActionRate[eventType]
                )
                userHourlyActionRate.append(eventTypeHourlyActionRate)

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

    def storeStatistics(self):
        self.checkStatFolder()
        print "store user is"
        self.storeUserID()
        print "store obj is"
        self.storeObjID()
        print "store user action rate"
        self.storeUserActionRate()
        print "store object preference"
        self.storeUserObjectPreference()



if __name__ == '__main__':
    start = time.time()
    independentAnalysisLib = IndependentAnalysisLib()
    end = time.time()
    print("Analyze time: %f"%(end-start))

    # for userId in independentAnalysisLib.userHourlyActionRate:
    #     for eventType in independentAnalysisLib.eventTypes:
    #         print("UserID: %s, EventType: %s, HourlyRate: "%(userId, eventType),
    #               independentAnalysisLib.userHourlyActionRate[userId][eventType])
    # for eventType in independentAnalysisLib.eventTypes:
    #     print(eventType, independentAnalysisLib.generalHourlyActionRate[eventType])
