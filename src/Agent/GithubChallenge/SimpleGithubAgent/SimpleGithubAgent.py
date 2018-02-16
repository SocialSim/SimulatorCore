import random
from BehaviorModel.BernoulliModel import BernoulliModel

class Agent():
    '''
    A simple Agent model for GitHub users. The users perform independent actions
    where the rates of actions were computed from the database by the AnalysisLib.
    '''

    ''' Init function '''
    def __init__(self, unique_id, analysis_lib, attributes):
        self.id = unique_id
        self.analysisLib = analysis_lib
        self.attributes = attributes

    ''' Function to perform for every step'''			
    def step(self, current_time):
        '''
        The step() function is used by TimeBasedSimulator. This function is 
        invoked at every time step in the simulation loop.

        :param currentTime: current simulation time
        :return: the list of instantaneous events gererated by the agent at 
            the given time.
        '''
        activity_history = list()

        object_list = self.analysisLib.getIds("objects")
        action_list = self.analysisLib.getActions()

        # For each interested repository
        for obj in object_list:
            # For each action type
            for i in range(len(action_list["action"])):
                indProb = self.analysisLib.getIndendentProbOfAgent(self.id, obj, action_list["action"][i], current_time % 24)
                # Flip a coin and see if I'm going to do any action on it
                if BernoulliModel.evaluate(indProb):
                    # Perform set of actions based on type of action
                    if action_list["definition"][i] == "singular":
                        if obj not in self.attributes[action_list["agent_attribute"][i]]:
                            self.attributes[action_list["agent_attribute"][i]].append({"id": obj, "timestamp": current_time})
                            activity_history.append([self.id, obj, action_list["action"][i], current_time])
                        else:
                            continue # this is not necessarily true
                    else:
                        self.attributes[action_list["agent_attribute"][i]].append({"id": obj, "timestamp": current_time})
                        activity_history.append([self.id, obj, action_list["action"][i], current_time])
                    break # the agent should only be able to take one action per time step

        return activity_history

    def updateAttributes(self, actorId, action, timestamp):
        self.attributes[action].append({"id": actorId, "timestamp": timestamp})
        pass

    def parseAttribute(self, attr):
        pass
        # query simulation table in db to get this agent's target attribute

    def returnAttributes(self):
        return self.attributes

    def returnId(self):
        return self.id

    def next(self, currentTime):
        '''
        The next() function is used by EventBasedSimulator.

        :param currentTime: current simulation time
        :return: the next event the agent generates in the nearest future.'''
        
        pass
