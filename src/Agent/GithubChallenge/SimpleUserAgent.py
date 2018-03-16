import random

from StatProxy.StatProxy import StatProxy
from BehaviorModel.SimpleBehaviorModel import SimpleBehaviorModel
from Agent.Agent import Agent


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
        
        statProxy = StatProxy.getInstance(agentType="simple")
        self.hourlyActionRates = statProxy.getUserHourlyActionRate(
            self.id)
        self.objectPreference = statProxy.getUserObjectPreference(
            self.id)

    def step(self):
        '''
        The step() function is used by TimeBasedSimulator. This function is invoked at every time step in the simulation loop.

        :param currentTime: current simulation time
        :return: the list of instantaneous events the agent generates between currentTime and currentTime+unitTime.
        '''

        # FIXME what if simulation time DOES NOT advance every one hour
        events = SimpleBehaviorModel.evaluate(self.hourlyActionRates,
                                              self.objectPreference)

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
