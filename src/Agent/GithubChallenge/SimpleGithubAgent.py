import random
from AnalysisLib.AnalysisLib import AnalysisLib
from BehaviorModel.SimpleBehaviorModel import SimpleBehaviorModel


class Agent():
    '''
    A simple Agent model for GitHub users. The user generates actions according to
    (i) the user's hourly action rate and
    (ii) the user's preference over the repos she is working on
    both of which were computed from the database using AnalysisLib.
    '''

    def __init__(self, agentId):
        self.agentId = agentId

        # Populate agent attribute with data
        self.__build()

    def __build(self):
        '''Query AnalysisLib to get an ObjectPreference instance and a list of HourlyActionRate instances.'''
        analysislib = AnalysisLib.getInstance()
        self.hourlyActionRates = analysislib.getAgentHourlyActionRate(
            self.agentId)
        self.objectPreference = analysislib.getAgentObjectPreference(
            self.agentId)

    def step(self, currentTime, unitTime):
        '''
        The step() function is used by TimeBasedSimulator. This function is invoked at every time step in the simulation loop.

        :param currentTime: current simulation time
        :return: the list of instantaneous events the agent generates at the given time.
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
