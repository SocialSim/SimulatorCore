import pickle

from common.const import *
from Dependency.ObjectPreference import *
from Dependency.HourlyActionRate import *
from Dependency.UserDependency import *

class StatProxy(object):

    _instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if StatProxy._instance is None:
            StatProxy()
        return StatProxy._instance
    
    def __init__(self):
        if StatProxy._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            StatProxy._instance = self

        self.allUserActionRate = None
        self.allObjectPreference = None
        self.allUserDependency = None
        self.userIDs= None
        self.objIDs= None

        self.retrieveStatistics()

    def retrieveStatistics(self):
        self.retrieveUserIDs()
        self.retrieveObjIDs()
        self.retrieveUserActionRate()
        self.retrieveObjectPreference()
        self.retrieveUserDependency()

    def retrieveUserIDs(self):
        self.userIDs = pickle.load(open(USER_ID_FILE, "rb" ))

    def retrieveObjIDs(self):
        self.objIDs= pickle.load(open(OBJ_ID_FILE, "rb" ))

    def retrieveUserActionRate(self):
        self.allUserActionRate = pickle.load(open(USER_ACTION_RATE_FILE, "rb" ))

    def retrieveObjectPreference(self):
        self.allObjectPreference = pickle.load(open(OBJECT_PREFERENCE_FILE, "rb" ))

    def retrieveUserDependency(self):
        self.allUserDependency = pickle.load(open(USER_DEPENDENCY_FILE, "rb" ))

    def getUserIds(self):
        return self.userIDs

    def getObjectIds(self):
        return self.objIDs

    def getUserHourlyActionRate(self, userId):
        '''
        :return: a list of HourlyActionRate instances, one for each actionType 
        '''
        if userId in self.userIDs:
            return self.allUserActionRate[userId]
        else:  #This is a new user, no record.
            return self.allUserActionRate[-1]

    def getUserObjectPreference(self, userId):
        '''
        :return: an ObjectPreference instance
        '''
        if userId in self.userIDs:
            return self.allObjectPreference[userId]
        else:  #This is a new user, no record.
            return self.allObjectPreference[-1]

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
