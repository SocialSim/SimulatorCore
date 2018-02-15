import random
from AnalysisLib.AnalysisLib import AnalysisLib
from BehaviorModel.BernoulliModel import BernoulliModel


class Agent():
    '''A simple Agent model for GitHub users. The users perform independent actions where the rates of actions were computed from the database by the AnalysisLib.'''
    def __init__(self, agentId):
        self.agentId = agentId
        self.behaviorModel = BernoulliModel()

        # Populate agent attribute with data
        self.__build()

        
    def __build(self):
        '''Query AnalysisLib to get probabilities of independent actions.'''
        self.indActions = AnalysisLib.getAgentIndependentActions(self.agentId)

        
    def step(self, currentTime):
        '''Used by TimeBasedSimulator. This function is invoked at every time step in the simulation loop. It returns the list of events gererated by the agent at the current time.'''
        events = []

        for indAction in self.indActions:
            if self.behaviorModel.evaluate(indAction):
                event = [indAction.agentId, indAction.objectId, indAction.actionType, currentTime]
                print(event)
                events.append(event)

        return events

    
    def next(self, currentTime):
        '''Used by EventBasedSimulator. It returns the next events the agent is going to generate, including the timestamp of the event.'''
        pass
