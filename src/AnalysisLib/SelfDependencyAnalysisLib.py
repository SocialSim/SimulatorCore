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
from Dependency.ClusterMember import ClusterMember
from sklearn.cluster import KMeans
from IndependentAnalysisLib import IndependentAnalysisLib
from ClusIndependentAnalysisLib import ClusIndependentAnalysisLib


class SelfDependencyAnalysisLib(ClusIndependentAnalysisLib):
    _instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if SelfDependencyAnalysisLib._instance is None:
            SelfDependencyAnalysisLib()
        return SelfDependencyAnalysisLib._instance

    def __init__(self , fileName = None):
        if SelfDependencyAnalysisLib._instance is not None:
            raise Exception("SelfDependencyAnalysisLib class is a singleton!")
        else:
            SelfDependencyAnalysisLib._instance = self

        # Perform the analysis in ClusIndependentAnalysisLib
        super(SelfDependencyAnalysisLib, self).__init__(fileName)

        # Store the user dependencies
        self.userSelfDependency = {}
        self.userObjectLastActionType = {}

        # Init user dependencies
        self.initUserSelfDependency()
        self.initUserObjectLastActionType()

        # Find the user dependencies.
        print("User self dependency pass...")
        self.userSelfDependencyPass()

    def initUserSelfDependency(self):
        '''
        Initialize the dependencies of each ACTIVE user
        :return:
        '''
        for userId in self.userIds:
            if self.isActiveUser(userId):
                self.userSelfDependency[userId] = {}
                for leftType in CORE_EVENT_TYPES:
                    self.userSelfDependency[userId][leftType] = {}
                    for rightType in CORE_EVENT_TYPES:
                        self.userSelfDependency[userId][leftType][rightType] = float(0)

    def initUserObjectLastActionType(self):
        '''
        Initialize the event type of each ACTIVE user on his repos.
        Only consider the repos that the actiev users frequently work on.
        :return:
        '''
        for userId in self.userIds:
            if self.isActiveUser(userId):
                self.userObjectLastActionType[userId] = {}
                for objectId in self.userObjectCount[userId]:
                    if self.userObjectCount[userId][objectId] > 2:
                        self.userObjectLastActionType[userId][objectId] = None

    def userSelfDependencyPass(self):
        '''
        Extract the pairwise dependencies between different types on the same repo by same user.
        :return:
        '''

        with open(self.fileName, "r") as file:
            for line in file:
                if not line:
                    break
                else:
                    line = line.strip('\n')
                    eventTime, hour, objectId, userId, eventType = self.eventSplit(line)

                    # Skip the events types that we do not care.
                    if eventType not in self.coreEventTypes:
                        continue

                    if userId in self.userSelfDependency:
                        if objectId in self.userObjectLastActionType[userId]:
                            if self.userObjectLastActionType[userId][objectId]:
                                preEventType = self.userObjectLastActionType[userId][objectId]
                                self.userSelfDependency[userId][preEventType][eventType] += 1
                            self.userObjectLastActionType[userId][objectId] = eventType

        # Summarize the user self dependency
        for userId in list(self.userSelfDependency):
            for eventType in CORE_EVENT_TYPES:
                typeCount = float(sum(self.userSelfDependency[userId][eventType].values()))
                if typeCount > 0:
                    for postType in CORE_EVENT_TYPES:
                        self.userSelfDependency[userId][eventType][postType] /= typeCount
                else:
                    del self.userSelfDependency[userId][eventType]

        # Remove the unqualified dependencies
        for userId in list(self.userSelfDependency):
            for leftType in list(self.userSelfDependency[userId]):
                for rightType in list(self.userSelfDependency[userId][leftType]):

                    rightIndex = self.coreEventTypes[rightType]
                    generalProbability = self.userTypeDistribution[userId][rightIndex]
                    dependentProbability = self.userSelfDependency[userId][leftType][rightType]

                    if generalProbability <= 0.05 or dependentProbability <= 1.3 * generalProbability:
                        del self.userSelfDependency[userId][leftType][rightType]

                if not self.userSelfDependency[userId][leftType]:
                    del self.userSelfDependency[userId][leftType]

            if not self.userSelfDependency[userId]:
                del self.userSelfDependency[userId]

    def getUserSelfDependency(self, userId):
        '''
        Return the dependnecies among different event types for the given user.
        :param userId:
        :return:
        '''
        if userId in self.userSelfDependency:
            return self.userSelfDependency[userId]


if __name__ == '__main__':
    start = time.time()
    fileName = sys.argv[1]
    analysisLib = SelfDependencyAnalysisLib(fileName)
    end = time.time()
    print("Analyze time: %f" % (end - start))

    print("-----------------------------------------------------------------------")
    print("Inactive user number: %d" % analysisLib.inactiveUserCount)
    print("Inactive user event number: %d" % analysisLib.inactiveTotalActionCount)
    print("-----------------------------------------------------------------------")
    print("Regular user number: %d" % analysisLib.regularUserCount)
    print("Regular user event number: %d" % analysisLib.regularTotalActionCount)
    print("-----------------------------------------------------------------------")
    print("Active user number: %d" % analysisLib.activeUserCount)
    print("Active user event number: %d" % analysisLib.activeTotalActionCount)

    for userId in analysisLib.userSelfDependency:
        print("-------------------------" + userId + "-------------------------")
        dependency = analysisLib.getUserSelfDependency(userId)
        for leftType in dependency:
            for rightType in dependency[leftType]:

                rightIndex = analysisLib.coreEventTypes[rightType]
                generalProbability = analysisLib.userTypeDistribution[userId][rightIndex]
                dependentProbability = dependency[leftType][rightType]

                print("%s --> %s" % (leftType, rightType))
                print("General probability: %f" % generalProbability)
                print("Dependent probability: %f" % dependentProbability)
                print(" ")

