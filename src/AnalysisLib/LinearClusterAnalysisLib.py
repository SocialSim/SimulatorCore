from common.const import *
import numpy as np
from collections import deque
import copy, time, json, sys
import common.analysisArgParser as argParser
import matplotlib.pyplot as plt

from Dependency.ObjectPreference import ObjectPreference
from Dependency.HourlyActionRate import HourlyActionRate
from Dependency.TypeDistribution import TypeDistribution
from IndependentAnalysisLib import IndependentAnalysisLib

class LinearClusterAnalysisLib(IndependentAnalysisLib):
    '''
    A simple clustering algorithm which puts user touching the same repo into 
    the same community
    '''

    @staticmethod
    def getInstance():
        if LinearClusterAnalysisLib._instance is None:
            LinearClusterAnalysisLib()
        return LinearClusterAnalysisLib._instance

    def __init__(self , fileName = None):
        LinearClusterAnalysisLib._instance = self

        # Two passes to get the typeDistribution and hourlyActionRate for REGULAR users and ACTIVE users
        super(LinearClusterAnalysisLib, self).__init__(fileName)

        # Initialize all the member variables
        self.__init__members()

        # Do one more clustering for regular users.
        self.clusterUser()

    def __init__members(self):
        self.objToClusterID = dict()
        # NOTE: each user can only associate with one cluster
        self.userToClusterID = dict() 

    def clusterUser(self):
        '''
        Used to cluster the REGULAR users based on their type distribution and hourly rate.
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

                    if objectId not in self.objToClusterID:
                        self.objToClusterID[objectId] = len(self.objToClusterID)

                    self.userToClusterID[userId] = self.objToClusterID[objectId]

    def storeUserID(self):
        with open(USER_ID_FILE, 'w') as thefile:
            for item in self.userIds:
                  thefile.write("%s %s\n" % (item, str(self.userToClusterID[item])))

    def storeStatistics(self):
        super(LinearClusterAnalysisLib, self).storeStatistics()

if __name__ == '__main__':
    start = time.time()
    fileName = sys.argv[1]
    analysisLib = ClusIndependentAnalysisLib(fileName)
    # analysisLib.storeStatistics()
    end = time.time()
    print("Analyze time: %f s" % (end - start))
    print("-----------------------------------------------------------------------")
    print("Inactive user number: %d" % analysisLib.inactiveUserCount)
    print("Inactive user event number: %d" % analysisLib.inactiveTotalActionCount)
    print("-----------------------------------------------------------------------")
    print("Regular user number: %d" % analysisLib.regularUserCount)
    print("Regular user event number: %d" % analysisLib.regularTotalActionCount)
    print("-----------------------------------------------------------------------")
    print("Active user number: %d" % analysisLib.activeUserCount)
    print("Active user event number: %d" % analysisLib.activeTotalActionCount)
    print("-----------------------------------------------------------------------")

    for clusterId in analysisLib.clusterIds:
        print("User number of %s: %d, event number: %d" %
              (clusterId, len(analysisLib.clusterMembers[clusterId]), analysisLib.clusterIds[clusterId]))

