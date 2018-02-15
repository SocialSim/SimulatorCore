import random
from AnalysisLib.AnalysisLib import AnalysisLib


class Agent():
    '''A simple Agent model for GitHub users. The users perform independent actions where the rates of actions were computed from the database by the AnalysisLib.'''
    def __init__(self, agentId):
        self.id = agentId
        self.analysisLib = AnalysisLib()
        

    def build(self):
        '''Query AnalysisLib to get probabilities of independent actions.'''
        self.indProb = self.analysisLib.getIndendentProbOfAgent(self.id)

        
    def step(self, currentTime):
        '''Used by TimeBasedSimulator. This function is invoked at every time step in the simulation loop. It returns the list of events gererated by the agent at the current time.'''
        events = []

        # For each interested Github repository
        for obj in self.indProb.keys():
            # For each action type
            for actionType in self.indProb[obj]:
                prob = self.indProb[obj][actionType][currentTime % 24]
                
                # Flip a coin and see if I'm going to do any action on it
                if random.random() <= prob:
                    events.append([self.id,obj,actionType,currentTime])

        return events

    
    def next(self, currentTime):
        '''Used by EventBasedSimulator. It returns the next events the agent is going to generate, including the timestamp of the event.'''
        pass
