import random

from AnalysisLib.AnalysisLib import AnalysisLib
from BehaviorModel.SimpleBehaviorModel import SimpleBehaviorModel
from BehaviorModel.DependentBehaviorModel import DependentBehaviorModel
from DependencyLogger.DependencyLogger import DependencyLogger
from Agent.Agent import Agent
from SimpleUserAgent import SimpleUserAgent


class DependentUserAgent(SimpleUserAgent):
    '''
    A Dependent Agent model for GitHub users. The user generates actions according to
    (i) Independent behaviors
    (2) Dependent actions according to his dependency relationships
    both of which were computed from the database using AnalysisLib.
    '''

    def __init__(self, id):
        super(DependentUserAgent, self).__init__(id)

        # Populate agent attribute with data
        self.build()

    def build(self):
        '''Query AnalysisLib to get an ObjectPreference instance and a list of HourlyActionRate instances, as
        well as the userDependency relationships.'''

        analysislib = AnalysisLib.getInstance()
        self.hourlyActionRates = analysislib.getUserHourlyActionRate(
            self.id)
        self.objectPreference = analysislib.getUserObjectPreference(
            self.id)
        self.userDependency = analysislib.getUserDependency(self.id)

    def step(self, currentTime, unitTime):
        '''
        The step() function is used by TimeBasedSimulator. This function is invoked at every time step in the simulation loop.

        :param currentTime: current simulation time
        :return: the list of instantaneous events the agent generates between currentTime and currentTime+unitTime.
        '''

        # FIXME what if simulation time DOES NOT advance every one hour
        independentEvents = SimpleBehaviorModel.evaluate(self.hourlyActionRates,
                                                         self.objectPreference,
                                                         currentTime, unitTime)
        dependentEvents = DependentBehaviorModel.evaluate(self.userDependency,
                                                          1,  # Same as the dependency length as in Analysislib
                                                          self.objectPreference,
                                                          currentTime, unitTime)
        events = independentEvents + dependentEvents
        return events

    def next(self, currentTime):
        '''
        The next() function is used by EventBasedSimulator.

        :param currentTime: current simulation time
        :return: the next event the agent generates in the nearest future.'''

        pass
