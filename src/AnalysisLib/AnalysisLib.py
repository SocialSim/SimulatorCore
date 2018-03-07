from common.const import *
import numpy as np
from collections import deque
import copy

from Dependency.ObjectPreference import ObjectPreference
from Dependency.HourlyActionRate import HourlyActionRate
from Dependency.UserDependency import UserDependency

FILE_NAME = DATAPATH + "/compressed_event_2015-01-01.txt"

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

        self.dependencyTimeLength = 3600 #Initially set the dependency window size as one hour
        self.activityThreshold = 3 #Users with activities over this threshold will be set as active users.
        self.dependencyThreshold = 0.2 # We will only set the dependency if the conditional prob is over this threshold.
        self.dependencyWindow = deque() #Use a queue to represent the events within the dependency time window
        self.userIds = []
        self.objectIds = []
        self.eventTypes = ["CommitCommentEvent", "CreateEvent", "DeleteEvent", "ForkEvent", "IssueCommentEvent",
                           "IssuesEvent", "PullRequestEvent", "PushEvent", "WatchEvent", "PublicEvent",
                           "MemberEvent", "GollumEvent", "ReleaseEvent", "PullRequestReviewCommentEvent"]
        self.userObjectPreference = {}
        self.userHourlyActionRate = {} #Should only count the independent actions, specific to event types.
        self.userTotalActionCount = {}
        self.userDependencies = {}
        self.generalTypeActionCount = {} # The general count of actions belonging to each type.
        self.generalObjectPreference = {}
        self.generalHourlyActionRate = self.initializeHourlyDistributions()


        #The first pass, we determine the initial dependencies, and user hourly action rate
        self.firstPass()

        #Extract the denpendencies, remove the unqualified dependency relationships
        for userId in self.userIds:
            for dependentUserId in self.userDependencies[userId]:
                self.userDependencies[userId][dependentUserId] /= self.userTotalActionCount[dependentUserId]
            self.extractUserDependency(userId)

        #Extract the general hourlyActionRate and objectPreference
        self.summarizeGeneralDistribtions()

        #The second pass, extract the independent actions.
        self.secondPass()

        #Update the userHourActionRate and userObjectPreference
        self.summarizeUserDistributions()


    def firstPass(self):
        '''
        The first pass, we determine the initial dependencies, and user hourly action rate
        Will clean the dependencies, and do a seconde pass to update the independent actions
        :return:
        '''
        with open(FILE_NAME, "r") as file:
            for line in file:
                if not line:
                    break
                else:
                    line = line.strip('\n')
                    eventTime, hour, objectId, userId, eventType = self.eventSplit(line)
                    #update the dependencyWindow
                    self.updateDependencyWindow(eventTime)
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
                        #Update the userDependencies
                        self.addUserDependency(userId, "new")

                    else:  #Not a new user.
                        self.userTotalActionCount[userId] += 1
                        #Update the userHourlyActionRate
                        self.updateUserHourlyActionRate(userId, hour, eventType, "old")
                        #Update the userObjectPreference
                        self.updateUserObjectPreference(userId, objectId, "old")
                        # Update the userDependencies
                        self.addUserDependency(userId, "old")

                    #Update the general hourlyActionRate and objectPreference
                    self.updateGeneralDistributions(objectId, hour, eventType)

                    # Append this event to the dependnecy window
                    self.dependencyWindow.append([eventTime, objectId, userId])

    def secondPass(self):
        '''
        The second pass will use the dependency information from the first pass to extract the independent actions.
        :return:
        '''
        self.dependencyWindow.clear()
        with open(FILE_NAME, "r") as file:
            for line in file:
                if not line:
                    break
                else:
                    line = line.strip('\n')
                    eventTime, hour, objectId, userId, eventType = self.eventSplit(line)
                    # update the dependencyWindow
                    self.updateDependencyWindow(eventTime)
                    #Update the independent actions.
                    if not self.isIndependentAction(userId):
                        self.userHourlyActionRate[userId][eventType][hour] -= 1 #FIXME: some problems here

                    # Append this event to the dependnecy window
                    self.dependencyWindow.append([eventTime, objectId, userId])

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

    def addUserDependency(self, userId, userType):
        '''
        Used in the first pass, we will add all the possible dependencies for the user.
        :param userId: the user for whom we want to update his dependencies
        '''
        candidateUsers = self.candidateDependentUsers()
        if userType == "new":
            self.userDependencies[userId] = {}
        for dependentUserId in candidateUsers:
            if dependentUserId == userId:
                continue
            elif dependentUserId not in self.userDependencies[userId]:
                self.userDependencies[userId][dependentUserId] = 1.0
            else:
                #Avoid conditions like (..., a, b, b) one-to-multiple dependencies
                #We need to guarantee there is no userId between userId and dependentUserId
                userSequence = list(event[2] for event in self.dependencyWindow)
                flag = True
                for user in userSequence:
                    if user == userId:
                        flag = False
                    elif user == dependentUserId:
                        flag = True
                if flag:
                    self.userDependencies[userId][dependentUserId] += 1

    def extractUserDependency(self, userId):
        '''
        This function will remove the un-qualified user dependencies.
        :param userId:
        '''
        for dependentUserId in list(self.userDependencies[userId].keys()):
            if not self.isActiveUser(dependentUserId):
                del(self.userDependencies[userId][dependentUserId])
            elif not self.isQualifiedDependency(userId, dependentUserId):
                del(self.userDependencies[userId][dependentUserId])

    def candidateDependentUsers(self):
        '''
        :return: Return the subset of users in current dependency window, remove the redundant guys.
        '''
        candidateUsers = []
        for event in self.dependencyWindow:
            eventUserId = event[2]
            if not eventUserId in candidateUsers:
                candidateUsers.append(eventUserId)
        return candidateUsers

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

    def isQualifiedDependency(self, userId, dependentUserId):
        '''
        Judge whether the given user pair is a qualified dependency relationship.
        :param userId:
        :param dependentUserId:
        :return:
        '''
        return self.userDependencies[userId][dependentUserId] > self.dependencyThreshold

    def isIndependentAction(self, userId):
        '''
        Judge whether the given action is independent.
        :param userId:
        :return:
        '''
        candidateUsers = self.candidateDependentUsers()
        for dependentUser in candidateUsers:
            if dependentUser in self.userDependencies[userId]:
                return False
        return True

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

    def getUserDependency(self, userId):
        '''
        Return: the dependency this user has from the hitory.
        :param userId:
        :return: A dictionary of his dependent relationship.
        '''
        if userId in self.userIds:
            userDependency = UserDependency(
                userId, self.userDependencies[userId]
            )
        else:
            userDependency = UserDependency(
                userId, dict())
        return userDependency

    def getUserDependentActions(self, userID):
        return None


if __name__ == '__main__':
    analysislib = AnalysisLib()
    # for userId in analysislib.userIds:
    #     if analysislib.getUserDependency(userId).userDependency:
    #         print("User Id: %s"%userId, "number of actions: %d"%analysislib.userTotalActionCount[userId],
    #               "dependencies: ", analysislib.getUserDependency(userId).userDependency)
        # print(analysislib.userTotalActionCount[userId])
        # print(analysislib.userHourlyActionRate[userId])
    for eventType in analysislib.eventTypes:
        print(eventType, analysislib.generalTypeActionCount[eventType])
        # print(eventType, analysislib.generalHourlyActionRate[eventType])