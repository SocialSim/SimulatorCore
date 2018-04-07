import warnings
warnings.filterwarnings("ignore")

from common.const import *
import numpy as np
import pandas as pd
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
from pathos.multiprocessing import Pool
from pathos.multiprocessing import cpu_count
from functools import partial

class UserDependencyAnalysisLib(IndependentAnalysisLib):
    '''
    We find the dependencies between active users here. The dependencies are modeled as (u1, a1) --> (u2, a2) on the
    same repo. They have to be performed on the same repo, but the user dependencies are not repo-specific.
    '''
    _instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if UserDependencyAnalysisLib._instance is None:
            UserDependencyAnalysisLib()
        return UserDependencyAnalysisLib._instance

    def __init__(self, fileName = None):
        if UserDependencyAnalysisLib._instance is not None:
            raise Exception("UserDependencyAnalysisLib class is a singleton!")
        else:
            UserDependencyAnalysisLib._instance = self

        # Perform the analysis in UserDependencyAnalysisLib
        super(UserDependencyAnalysisLib, self).__init__(fileName)

        # Store the user dependencies
        # NOTE: We only consider the dependencies between ACTIVE users, and on the popular repos.
        # Key: (u1, a1, u2, a2) Value: P(u1, a1, u2, a2) / P(u1, a1)
        self.userDependency = {}
        self.userDependencyCount = {}

        # Store the number of actions of active users
        self.userTypeCountInBuff = {}

        # This structure stores the recent events of POPULAR repos by active users.
        self.buff = []
        self.objectIdsInBuff = []

        # Extract the related events into the buff
        print("Extracting data...")
        self.extractData()

        # Count the number of occurences of (user, action) pair in buffer.
        print("Counting buffer...")
        self.countBuff()

        # Analyze the dependency from the bufferd events
        print("Countinng dependency...")
        self.countDependency()

        print("Analyzing dependency...")
        self.analyzeDependency()


    def extractData(self):
        '''
        Extract the events of ACTIVE users on POPULAR objects with CORE event types.
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
                    # Only consider the active users' dependencies.
                    if not self.isActiveUser(userId):
                        continue
                    # Only consider the active repos.
                    if not self.isPopularObject(objectId):
                        continue

                    self.buff.append([eventTime, objectId, userId, eventType])


    def countBuff(self):
        '''
        This function counts the (user, action) occurence times in the buffer.
        :return:
        '''
        df = pd.DataFrame(data=self.buff, columns=['eventTime', 'objectId', 'userId', 'eventType'])

        candidateObjectIds = df.objectId.unique().tolist()
        for objectId in candidateObjectIds:
            pdf = df[df.objectId == objectId].reset_index(drop=True)
            if len(pdf.userId.unique()) > 1 or len(pdf.eventType.unique()) > 1:
                self.objectIdsInBuff.append(objectId)

        df = df.drop(labels=['eventTime', 'objectId'], axis=1)
        df['value'] = 1
        df = df.groupby(['userId', 'eventType']).sum()
        self.userTypeCountInBuff = df.value.to_dict()


    @staticmethod
    def analyzeObject(objectId, df):
        '''
        Analyze user dependency of the give object.
        :param df:
        :param objectId:
        :return:
        '''
        pdf = df[df.objectId == objectId].reset_index(drop=True)
        pdf = pdf.sort_values(by='eventTime')
        pdf = pdf.drop(labels=['objectId'], axis=1)

        # Remove the consecutive same type actions by same users on the same repo.
        userId = ' '
        eventType = ' '
        flagList = []
        for row in pdf.itertuples():
            if row.userId == userId and row.eventType == eventType:
                flagList.append(False)
            else:
                flagList.append(True)
                userId = row.userId
                eventType = row.eventType
        pdf = pdf.loc[flagList, :].reset_index(drop=True)

        dependencyCount = {}
        preUserId = ''
        preEventType = ''
        for row in pdf.itertuples():
            if preUserId and preEventType:
                if (preUserId, preEventType, row.userId, row.eventType) in dependencyCount:
                    dependencyCount[(preUserId, preEventType, row.userId, row.eventType)] += 1
                else:
                    dependencyCount[(preUserId, preEventType, row.userId, row.eventType)] = 1.0
            preUserId = row.userId
            preEventType = row.eventType

        return dependencyCount


    def countDependency(self):
        '''
        Count the user dependency from the buffer.
        :return:
        '''
        df = pd.DataFrame(data=self.buff, columns=['eventTime', 'objectId', 'userId', 'eventType'])
        df.eventTime = pd.to_datetime(df.eventTime)

        nCPU = cpu_count()
        pool = Pool(nCPU)
        analyzeObject_partial = partial(UserDependencyAnalysisLib.analyzeObject, df=df)
        integratedDependencyCount = pool.map(analyzeObject_partial, self.objectIdsInBuff)
        pool.close()
        pool.join()
        for dependencyCount in integratedDependencyCount:
            self.userDependencyCount.update(dependencyCount)


    def analyzeDependency(self):
        '''
        According to the counted dependency number, summarize and filter the user dependency.
        :return:
        '''
        # Set the pandas display
        pd.set_option('display.width', None)

        df = pd.DataFrame(data=self.userDependencyCount.items(),
                          columns=['key', 'value'])

        df = df.groupby(['key']).sum().reset_index()
        df = df[df['value'] > 5]
        df[['leftUser', 'leftType', 'rightUser', 'rightType']] = df['key'].apply(pd.Series)
        df = df.drop(labels=['key'], axis=1).reset_index(drop=True)
        print df
        print(' ')

        tdf = df.drop(labels=['leftUser', 'rightUser'], axis=1).reset_index(drop=True)
        tdf = tdf.groupby(['leftType', 'rightType']).sum().reset_index()
        tdf = tdf[tdf['value'] > 30].reset_index(drop=True)
        print tdf
        print(' ')

        udf = df.drop(labels=['leftType', 'rightType'], axis=1).reset_index(drop=True)
        udf = udf.groupby(['leftUser', 'rightUser']).sum().reset_index()
        udf = udf[udf['value'] > 30].reset_index(drop=True)
        udf = udf[udf['leftUser'] != udf['rightUser']].reset_index(drop=True)
        print udf


if __name__ == '__main__':
    start = time.time()
    fileName = sys.argv[1]
    analysisLib = UserDependencyAnalysisLib(fileName)
    end = time.time()
    print("Analyzing time: %f s" % (end-start))

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
    print("Popular object number: %d" % len(analysisLib.objectIdsInBuff))