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


class ClusIndependentAnalysisLib(IndependentAnalysisLib):
    @staticmethod
    def getInstance():
        """ Static access method. """
        if ClusIndependentAnalysisLib._instance is None:
            ClusIndependentAnalysisLib()
        return ClusIndependentAnalysisLib._instance

    def __init__(self , fileName = None):
        ClusIndependentAnalysisLib._instance = self

        # Two passes to get the typeDistribution and hourlyActionRate for REGULAR users and ACTIVE users
        super(ClusIndependentAnalysisLib, self).__init__(fileName)

        self.rateClusterNum = 10
        self.typeClusterNum = 6

        self.regularUserIds = []
        self.clusterResult = []
        self.clusterIds = {}
        self.clusterHourlyActionRate = {}
        self.clusterTypeDistribution = {}
        self.clusterMembers = {}

        self.inactiveMembers = {}

        # Do one more clustering for regular users.
        self.userClustering()


    def userClustering(self):
        '''
        Used to cluster the REGULAR users based on their type distribution and hourly rate.
        :return:
        '''
        # Prepare the REGULAR users.
        hourlyRateAttributes = []
        typeAttributes = []

        for userId in self.userIds:
            if self.isActiveUser(userId):
                continue
            elif self.isInactiveUser(userId):
                self.inactiveMembers[userId] = self.userIds[userId]
            else:
                self.regularUserIds.append(userId)
                hourlyRateAttributes.append(self.userHourlyActionRate[userId])
                typeAttributes.append(self.userTypeDistribution[userId])

        # Do the clustering according to users hourly rate
        start = time.time()
        rateCluster = KMeans(n_clusters=self.rateClusterNum, max_iter=200, tol=0.001, n_jobs=-1)
        typeCluster = KMeans(n_clusters=self.typeClusterNum, max_iter=200, tol=0.001, n_jobs=-1)
        rateResult = np.array(rateCluster.fit_predict(hourlyRateAttributes))
        typeResult = np.array(typeCluster.fit_predict(typeAttributes))
        end = time.time()
        print("Clustering time: %f s" % (end-start))

        # Assign the clustering result
        self.clusterResult = rateResult * self.typeClusterNum + typeResult

        for i in range(self.rateClusterNum):
            for j in range(self.typeClusterNum):
                clusterId = "cluster" + str(i * self.typeClusterNum + j)
                self.clusterIds[clusterId] = 0.0
                self.clusterHourlyActionRate[clusterId] = rateCluster.cluster_centers_[i]
                self.clusterTypeDistribution[clusterId] = typeCluster.cluster_centers_[j]
                self.clusterMembers[clusterId] = {}

        for i in range(self.regularUserCount):
            userId = self.regularUserIds[i]
            clusterNum = self.clusterResult[i]
            clusterId = "cluster" + str(clusterNum)
            self.clusterMembers[clusterId][userId] = self.userIds[userId]
            self.clusterIds[clusterId] += self.userIds[userId]

    def getClusterActionRate(self, clusterId):
        '''
        Else considers the inactive user cluster
        :param clusterId:
        :return:
        '''
        if clusterId in self.clusterHourlyActionRate:
            hourlyActionRate = HourlyActionRate(clusterId, self.clusterIds[clusterId]/ANALYSIS_LENGTH,
                                                self.clusterHourlyActionRate[clusterId])
        else:
            hourlyActionRate = HourlyActionRate(clusterId, self.inactiveTotalActionCount/ANALYSIS_LENGTH,
                                                self.inactiveHourlyActionRate)

        return hourlyActionRate

    def getClusterTypeDistribution(self, clusterId):
        '''
        Else considers the inactive user cluster
        :param clusterId:
        :return:
        '''
        if clusterId in self.clusterTypeDistribution:
            typeDistribution = TypeDistribution(clusterId, self.clusterTypeDistribution[clusterId])
        else:
            typeDistribution = TypeDistribution(clusterId, self.inactiveTypeDistribution)

        return typeDistribution

    def getClusterMembers(self, clusterId):
        '''
        Else considers the inactive user cluster
        :param clusterId:
        :return:
        '''
        if clusterId in self.clusterMembers:
            clusterMember = ClusterMember(clusterId, self.clusterMembers[clusterId])
        else:
            clusterMember = ClusterMember(clusterId, self.inactiveMembers)

        return clusterMember

    def storeStatistics(self):
        super(ClusIndependentAnalysisLib, self).storeStatistics()
        self.storeClusterID()
        self.storeClusterActionRate()
        self.storeClusterTypeDistribution()
        self.storeClusterMember()


    def storeClusterID(self):
        pickle.dump(self.clusterIds, open(CLUSTER_ID_FILE, 'w'))

    def storeClusterActionRate(self):
        allActionRate = dict()
        for clusterId in self.clusterHourlyActionRate:
            actionRate = self.getClusterActionRate(clusterId)
            allActionRate[clusterId] = actionRate

        inactiveRate = self.getClusterActionRate(-1)
        allActionRate[-1] = inactiveRate

        pickle.dump(allActionRate, open(CLUSTER_ACTION_RATE_FILE, 'w'))

    def storeClusterTypeDistribution(self):
        allTypeDistribtuion = dict()
        for clusterId in self.clusterTypeDistribution:
            typeDistribution = self.getClusterTypeDistribution(clusterId)
            allTypeDistribtuion[clusterId] = typeDistribution

        inactiveRate = self.getClusterTypeDistribution(-1)
        allTypeDistribtuion[-1] = inactiveRate

        pickle.dump(allTypeDistribtuion, open(CLUSTER_TYPE_DISTRIBUTION_FILE, 'w'))

    def storeClusterMember(self):
        allMember = dict()
        for clusterId in self.clusterMembers:
            member = self.getClusterMembers(clusterId)
            allMember[clusterId] = member

        inactiveMember = self.getClusterMembers(-1)
        allMember[-1] = inactiveMember

        pickle.dump(allMember, open(CLUSTER_MEMBER_FILE, 'w'))


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

