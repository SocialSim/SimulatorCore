import random

from StatProxy.StatProxy import StatProxy
from BehaviorModel.SimpleBehaviorModel import SimpleBehaviorModel
from Agent.Agent import Agent
from common.const import *
import random


class SimpleUserClusterAgent(Agent):
    '''
    An agent model for clustered users in Github. Each virtual agent will contain a set of inactive users.
    '''

    def __init__(self, clusterId):
        super(SimpleUserClusterAgent, self).__init__(clusterId)

        # Populate agent attribute with data
        self.build()

    def build(self):
        '''
        Query StatProxy to get ONE hourly rate, ONE type distribution, and a list of object preference.
        - Hourly Rate: Consistent within one cluster.
        - Type Distribution: Consistent within one cluster.
        - Object Preference: specialized for each user.
        '''

        statProxy = StatProxy.getInstance(analysisLib="simple")
        self.hourlyActionRate = statProxy.getClusterHourlyActionRate(self.id)
        self.typeDistribution = statProxy.getClusterTypeDistribution(self.id)
        self.members = statProxy.getClusterMember(self.id).getMembers()

        self.scheduleQueue = []
        self.pointer = 0

        self.memberObjectPreferences = {}
        for member in self.members:
            self.memberObjectPreferences[member] = statProxy.getUserObjectPreference(member)
            for _ in range(int(self.members[member])):
                self.scheduleQueue.append(member)

        random.shuffle(self.scheduleQueue)
        self.initCumulativeProbs()

    def initCumulativeProbs(self):
        '''
        From the given probability object preference and type distribution to get the cumulative distribution.
        :return:
        '''
        self.memberCumObjectPreference = {}

        for userId in self.members:
            self.memberCumObjectPreference[userId] = [0.0 for i in range(len(self.memberObjectPreferences[userId].probs))]

            for index in range(len(self.memberObjectPreferences[userId].probs)):
                if index == 0:
                    self.memberCumObjectPreference[userId][index] =\
                        self.memberObjectPreferences[userId].probs[0]
                else:
                    self.memberCumObjectPreference[userId][index] = \
                        self.memberCumObjectPreference[userId][index - 1] + \
                        self.memberObjectPreferences[userId].probs[index]

        self.cumTypeDistribution = [0 for i in range(len(CORE_EVENT_TYPES))]
        for index in range(len(CORE_EVENT_TYPES)):
            if index == 0:
                self.cumTypeDistribution[index] = self.typeDistribution.probs[0]
            else:
                self.cumTypeDistribution[index] = self.cumTypeDistribution[index - 1] + \
                                                  self.typeDistribution.probs[index]

    def scheduleUser(self):
        '''
        Get the user that will perform the next action.
        :return:
        '''
        userId = self.scheduleQueue[self.pointer]

        self.pointer += 1
        if self.pointer == len(self.scheduleQueue):
            self.pointer = 0
            random.shuffle(self.scheduleQueue)

        return userId

    def getMemberCumObjectPreference(self, userId):
        '''
        Get the cumulative object preference of the given user.
        :param userId:
        :return:
        '''
        return self.memberObjectPreferences[userId].getObjectIds(), self.memberCumObjectPreference[userId]

    def step(self):
        '''
        The step() function is used by TimeBasedSimulator. This function is invoked at every time step in the simulation loop.

        :return: the list of instantaneous events the agent generates between currentTime and currentTime+unitTime.
        '''

        # FIXME what if simulation time DOES NOT advance every one hour
        events = SimpleBehaviorModel.clusterEvaluate(self,
                                                     self.hourlyActionRate,
                                                     self.cumTypeDistribution,
                                                     self.memberObjectPreferences,
                                                     self.memberCumObjectPreference)

        return events

    def next(self, currentTime):
        '''
        The next() function is used by EventBasedSimulator.

        :param currentTime: current simulation time
        :return: the next event the agent generates in the nearest future.'''

        pass
