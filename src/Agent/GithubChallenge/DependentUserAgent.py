import random

from StatProxy.StatProxy import StatProxy
from BehaviorModel.SimpleBehaviorModel import SimpleBehaviorModel
from BehaviorModel.DependentBehaviorModel import DependentBehaviorModel
from Agent.Agent import Agent
from SimpleUserAgent import SimpleUserAgent


class DependentUserAgent(SimpleUserAgent):
    '''
    A Dependent Agent model for GitHub users. The user generates actions
    according to
    (1) Independent behaviors
    (2) Dependent actions according to his dependency relationships
    both of which were computed from the database using StatProxy.
    '''

    def __init__(self, id):
        super(DependentUserAgent, self).__init__(id)

        # Populate agent attribute with data
        self.build()

    def build(self):
        '''Query StatProxy to get an ObjectPreference instance and a list of
        HourlyActionRate instances, as well as the userDependency
        relationships.'''

        statProxy = StatProxy.getInstance(agentType="dependent")
        self.hourlyActionRates = statProxy.getUserHourlyActionRate(
            self.id)
        self.objectPreference = statProxy.getUserObjectPreference(
            self.id)
        self.userDependency = statProxy.getUserDependency(self.id)

    def step(self, currentTime, unitTime):
        '''
        The step() function is used by TimeBasedSimulator. This function is
        invoked at every time step in the simulation loop.

        :param currentTime: current simulation time
        :return: the list of instantaneous events the agent generates
        '''

        # FIXME what if simulation time DOES NOT advance every one hour
        independentEvents = SimpleBehaviorModel.evaluate(self.hourlyActionRates,
                                                         self.objectPreference)
        dependentEvents = DependentBehaviorModel.evaluate(self.userDependency,
                                                          1,  # Same as the dependency length as in StatProxy
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
