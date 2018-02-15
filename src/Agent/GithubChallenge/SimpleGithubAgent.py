import random
from AnalysisLib.AnalysisLib import AnalysisLib
from BehaviorModel.BernoulliModel import BernoulliModel


class Agent():
    '''
    A simple Agent model for GitHub users. The users perform independent actions where the rates of actions were computed from the database by the AnalysisLib.
    '''
    def __init__(self, agentId):
        self.agentId = agentId

        # Populate agent attribute with data
        self.__build()

        
    def __build(self):
        '''Query AnalysisLib to get a list of IndependentAction objects.'''
        self.indActions = AnalysisLib.getAgentIndependentActions(self.agentId)

        
    def step(self, currentTime):
        '''
        The step() function is used by TimeBasedSimulator. This function is invoked at every time step in the simulation loop.

        :param currentTime: current simulation time
        :return: the list of instantaneous events gererated by the agent at the given time.
        '''
        events = []

        for indAction in self.indActions:
            if BernoulliModel.evaluate(indAction):
                event = [indAction.agentId, indAction.objectId, indAction.actionType, currentTime]
                print(event)
                events.append(event)

        return events

    
    def next(self, currentTime):
        '''
        The next() function is used by EventBasedSimulator.

        :param currentTime: current simulation time
        :return: the next event the agent generates in the nearest future.'''
        
        pass
