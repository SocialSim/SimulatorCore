import os
from common.const import *
from Dependency.ObjectPreference import ObjectPreference
from Dependency.HourlyActionRate import HourlyActionRate

class AnalysisLib(object):
    _instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if IndependentAnalysisLib._instance is None:
            IndependentAnalysisLib()
        return IndependentAnalysisLib._instance

    def __init__(self):

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

        with open(USER_ACTION_RATE_FILE, 'w') as thefile:
            for item in allActionRate:
                thefile.write("%s %s\n" % (item, len(allActionRate[item])))
                for actionRate in allActionRate[item]:
                    thefile.write("%s\n" % actionRate)


    def storeUserObjectPreference(self):
        allObjectPreference = dict()
        for userId in self.userObjectPreference:
            objectPreference = self.getUserObjectPreference(userId)
            allObjectPreference[userId] = objectPreference

        newUserObjectPreference = self.getUserObjectPreference(-1)
        allObjectPreference[-1] = newUserObjectPreference

        with open(OBJECT_PREFERENCE_FILE, 'w') as thefile:
            for item in allObjectPreference:
                thefile.write("%s" % (allObjectPreference[item]))


if __name__ == '__main__':
    independentAnalysisLib = IndependentAnalysisLib()

