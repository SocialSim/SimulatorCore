import random

from StatProxy.StatProxy import StatProxy
from BehaviorModel.SimpleBehaviorModel import SimpleBehaviorModel
from Agent.Agent import Agent
from common.const import *


class SimpleUserAgent(Agent):
    '''
    A simple Agent model for GitHub users. The user generates actions according to
    (i) the user's hourly action rate and
    (ii) the user's preference over the repos she is working on
    both of which were computed from the database using StatProxy.
    '''

    def __init__(self, id):
        super(SimpleUserAgent, self).__init__(id)

        # Populate agent attribute with data
        self.build()

    def build(self):
        '''Query StatProxy to get an ObjectPreference instance and a list of HourlyActionRate instances.'''
        
        statProxy = StatProxy.getInstance(analysisLib="simple")
        self.hourlyActionRate = statProxy.getUserHourlyActionRate(self.id)
        self.typeDistribution = statProxy.getUserTypeDistribution(self.id)
        self.objectPreference = statProxy.getUserObjectPreference(self.id)
        self.objectIds = self.objectPreference.getObjectIds()

        self.initCumulativeProbs()

    def initCumulativeProbs(self):
        '''
        From the given probability object preference and type distribution to get the cumulative distribution.
        :return:
        '''
        self.cumObjectPreference = [0 for i in range(len(self.objectPreference.probs))]
        for index in range(len(self.objectIds)):
            if index == 0:
                self.cumObjectPreference[index] = self.objectPreference.probs[0]
            else:
                self.cumObjectPreference[index] = self.cumObjectPreference[index-1] + \
                                                  self.objectPreference.probs[index]

        self.cumTypeDistribution = [0 for i in range(7)]
        for index in range(7):
            if index == 0:
                self.cumTypeDistribution[index] = self.typeDistribution.probs[0]
            else:
                self.cumTypeDistribution[index] = self.cumTypeDistribution[index-1] + \
                                                  self.typeDistribution.probs[index]

    def step(self):
        '''
        The step() function is used by TimeBasedSimulator. This function is invoked at every time step in the simulation loop.

        :param currentTime: current simulation time
        :return: the list of instantaneous events the agent generates between currentTime and currentTime+unitTime.
        '''

        # FIXME what if simulation time DOES NOT advance every one hour
        # events = SimpleBehaviorModel.evaluate(self.hourlyActionRate,
        #                                       self.objectPreference,
        #                                       self.typeDistribution)
        events = SimpleBehaviorModel.userEvaluate(self.id,
                                                  self.hourlyActionRate,
                                                  self.objectIds,
                                                  self.cumObjectPreference,
                                                  self.cumTypeDistribution)

        # FIXME the current parameters are read from file, and can not be changed
        # for event in events: # Update the objectPreference for create and delete event.
        #     eventType = event.getEventType()
        #     objectId = event.getObjID()
        #     if eventType == "CreateEvent":
        #         self.objectPreference.addObject(objectId)
        #     elif eventType == "DeleteEvent":
        #         self.objectPreference.deleteObject(objectId)

        return events

    def next(self, currentTime):
        '''
        The next() function is used by EventBasedSimulator.

        :param currentTime: current simulation time
        :return: the next event the agent generates in the nearest future.'''

        pass
