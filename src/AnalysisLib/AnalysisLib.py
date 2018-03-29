import os
from common.const import *
from Dependency.ObjectPreference import ObjectPreference
from Dependency.HourlyActionRate import HourlyActionRate

class AnalysisLib(object):
    _instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if AnalysisLib._instance is None:
            AnalysisLib()
        return AnalysisLib._instance

    def __init__(self):
        AnalysisLib._instance = self

        self.userIds = {} #Store the user IDs, and their number of total actions.
        self.objectIds = {} #Store the obj IDs, and their number of total actions.
        self.userObjectPreference = {}
        self.userHourlyActionRate = {} #Should only count the independent actions, specific to event types.


    def getUserHourlyActionRate(self, userId):
        raise Exception("Please define how user hourly action rate is calculated")

    def getUserObjectPreference(self, userId):
        raise Exception("Please define how user object preference is calculated")

    def getUserDependentActions(self, userID):
        raise Exception("Please define how user dependency is calculated")

    def storeStatistics(self):
        raise Exception("Please define what statistics you want to store")

    def checkStatFolder(self):
        if not os.path.exists(STAT_PATH):
            os.makedirs(STAT_PATH)


    def storeUserID(self):
        with open(USER_ID_FILE, 'w') as thefile:
            for item in self.userIds:
                  thefile.write("%s\n" % item)


    def storeObjID(self):
        with open(OBJ_ID_FILE, 'w') as thefile:
            for item in self.objectIds:
                  thefile.write("%s\n" % item)


    def storeUserActionRate(self):
        allActionRate = dict()
        for userId in self.userHourlyActionRate:
            actionRate = self.getUserHourlyActionRate(userId)
            allActionRate[userId] = actionRate

        newUserActionRate = self.getUserHourlyActionRate(-1)
        allActionRate[-1] = newUserActionRate
        print allActionRate[-1]

        with open(USER_ACTION_RATE_FILE, 'w') as thefile:
            for item in allActionRate:
                thefile.write("%s %s\n" % (item, 1))
                thefile.write("%s\n" % allActionRate[item])


    def storeUserObjectPreference(self):
        allObjectPreference = dict()
        for userId in self.userObjectPreference:
            objectPreference = self.getUserObjectPreference(userId)
            allObjectPreference[userId] = objectPreference

        with open(USER_OBJECT_PREFERENCE_FILE, 'w') as thefile:
            for item in allObjectPreference:
                thefile.write("%s" % (allObjectPreference[item]))


if __name__ == '__main__':
    independentAnalysisLib = IndependentAnalysisLib()

