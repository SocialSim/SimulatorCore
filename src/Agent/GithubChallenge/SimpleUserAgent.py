import random

from AnalysisLib.AnalysisLib import AnalysisLib
from BehaviorModel.SimpleBehaviorModel import SimpleBehaviorModel
from Agent.Agent import Agent


class SimpleUserAgent(Agent):
    '''
    A simple Agent model for GitHub users. The user generates actions according to
    (i) the user's hourly action rate and
    (ii) the user's preference over the repos she is working on
    both of which were computed from the database using AnalysisLib.
    '''

    def __init__(self, id):
        super(SimpleUserAgent, self).__init__(id)

        # Populate agent attribute with data
        self.build()

    def build(self):
        '''Query AnalysisLib to get an ObjectPreference instance and a list of HourlyActionRate instances.'''
        
        analysislib = AnalysisLib.getInstance()
        self.hourlyActionRates = analysislib.getUserHourlyActionRate(
            self.id)
        self.objectPreference = analysislib.getUserObjectPreference(
            self.id)

    def step(self, currentTime, unitTime):
        '''
        The step() function is used by TimeBasedSimulator. This function is invoked at every time step in the simulation loop.

        :param currentTime: current simulation time
        :return: the list of instantaneous events the agent generates between currentTime and currentTime+unitTime.
        '''

        # FIXME what if simulation time DOES NOT advance every one hour
        events = SimpleBehaviorModel.evaluate(self.hourlyActionRates,
                                              self.objectPreference,
                                              currentTime, unitTime)

        return events

    def next(self, currentTime):
        '''
        The next() function is used by EventBasedSimulator.

        :param currentTime: current simulation time
        :return: the next event the agent generates in the nearest future.'''

        pass
