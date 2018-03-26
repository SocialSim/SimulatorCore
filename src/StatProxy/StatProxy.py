import pickle
import copy

from common.const import *
from Dependency.ObjectPreference import *
from Dependency.HourlyActionRate import *
from Dependency.TypeDistribution import *
from Dependency.UserDependency import *

class StatProxy(object):

    _instance = None

    @staticmethod
    def getInstance(analysisLib):
        """ Static access method. """
        if StatProxy._instance is None:
            StatProxy(analysisLib)
        return StatProxy._instance
    
    def __init__(self, analysisLib):
        if StatProxy._instance is not None:
            raise Exception("StatProxy class is a singleton!")
        else:
            StatProxy._instance = self

        self.allUserActionRate = None
        self.allObjectPreference = None
        self.allTypeDistribution = None
        self.userIDs = None
        self.objIDs = None

        self.clusterIDs = None
        self.allClusterMembers = None
        self.allClusterActionRate = None
        self.allClusterTypeDistribution = None

        if analysisLib == "dependent":
            self.allUserDependency = None

        self.retrieveStatistics(analysisLib)


    def retrieveStatistics(self, agentType):
        self.retrieveUserIDs()
        self.retrieveObjIDs()
        self.retrieveUserActionRate()
        self.retrieveTypeDistribution()
        self.retrieveObjectPreference()

        self.retrieveClusterIDs()
        self.retrieveClusterMembers()
        self.retrieveClusterActionRate()
        self.retrieveClusterTypeDistribution()

        if agentType == "dependent":
            self.retrieveUserDependency()

    def retrieveUserIDs(self):
        self.userIDs = pickle.load(open(USER_ID_FILE, "rb" ))

    def retrieveObjIDs(self):
        self.objIDs= pickle.load(open(OBJ_ID_FILE, "rb" ))

    def retrieveUserActionRate(self):
        self.allUserActionRate = pickle.load(open(USER_ACTION_RATE_FILE, "rb" ))

    def retrieveObjectPreference(self):
        self.allObjectPreference = pickle.load(open(USER_OBJECT_PREFERENCE_FILE, "rb" ))

    def retrieveTypeDistribution(self):
        self.allTypeDistribution = pickle.load(open(USER_TYPE_DISTRIBUTION_FILE, "rb"))

    def retrieveUserDependency(self):
        self.allUserDependency = pickle.load(open(USER_DEPENDENCY_FILE, "rb" ))

    def retrieveClusterIDs(self):
        self.clusterIDs = pickle.load(open(CLUSTER_ID_FILE, "rb" ))

    def retrieveClusterMembers(self):
        self.allClusterMembers = pickle.load(open(CLUSTER_MEMBER_FILE, "rb" ))

    def retrieveClusterActionRate(self):
        self.allClusterActionRate = pickle.load(open(CLUSTER_ACTION_RATE_FILE, "rb" ))

    def retrieveClusterTypeDistribution(self):
        self.allClusterTypeDistribution = pickle.load(open(CLUSTER_TYPE_DISTRIBUTION_FILE, "rb" ))

    def getUserIds(self):
        return self.userIDs

    def getObjectIds(self):
        return self.objIDs

    def getClusterIds(self):
        return self.clusterIDs

    def getUserHourlyActionRate(self, userId):
        '''
        Get the hourly action distribution for the given user.
        '''
        if userId in self.allUserActionRate:
            return self.allUserActionRate[userId]
        else:  #This is a new user, no record.
            return self.allUserActionRate[-1]

    def getClusterHourlyActionRate(self, clusterId):
        '''
        Get the hourly action distribution for the given cluster.
        :param clusterId:
        :return:
        '''
        if clusterId in self.allClusterActionRate:
            return self.allClusterActionRate[clusterId]
        else:
            return self.allClusterActionRate[-1]

    def getUserObjectPreference(self, userId):
        '''
        Get the object preference for the given user.
        Note: no preference for new user.
        '''
        return self.allObjectPreference[userId]

    def getUserTypeDistribution(self, userId):
        '''
        Get the type distribution for the given user.
        '''
        if userId in self.allTypeDistribution:
            return self.allTypeDistribution[userId]
        else:
            return self.allTypeDistribution[-1]

    def getClusterTypeDistribution(self, clusterId):
        '''
        Get the type distribution for the given cluster.
        :param clusterId:
        :return:
        '''
        if clusterId in self.allClusterTypeDistribution:
            return self.allClusterTypeDistribution[clusterId]
        else:
            return self.allClusterTypeDistribution[-1]

    def getClusterMember(self, clusterId):
        '''
        Get the members of the given cluster.
        :param clusterId:
        :return:
        '''
        if clusterId in self.allClusterMembers:
            return self.allClusterMembers[clusterId]
        else:
            return self.allClusterMembers[-1]

    def getUserDependency(self, userId):
        '''
        Return: the dependency this user has from the hitory.
        :param userId:
        :return: A dictionary of his dependent relationship.
        '''
        if userId in self.userIDs:
            return self.allUserDependency[userId]
        else:
            return self.allUserDependency[-1]
