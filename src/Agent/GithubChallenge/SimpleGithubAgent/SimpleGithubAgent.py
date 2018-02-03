from mesa import Agent
import random

# Note: right now, all the attrbutes of an agent should be passed from simulator during
# initialization. The reason behind this is that we want to minimize "point of
# contact" to analysis library for future maintanence. The other way to do it
# is that we only pass in agent_id, and initialize every other attribute as None.
# Then when github agent needs it, it then queries analysis library itself.
class SimpleGithubAgent(Agent):

    ''' Init function '''
    def __init__(self, unique_id, model, ind_prob):
        super().__init__(unique_id, model)
        self.id = unique_id
        self.ind_prob = ind_prob

    ''' Function to perform for every step'''
    def step(self):
        current_time = self.model.current_time

        # For each interested repository
        for obj in self.ind_prob.keys():
            # For each action type
            for action_type in self.ind_prob[obj]:
                prob = self.ind_prob[obj][action_type][current_time % 24]
                print("UserId=%d, RepoId=%d, ActionType=%s, prob=%.3f"%(self.id, obj, action_type, prob))
                # Flip a coin and see if I'm going to do any action on it
                if random.random() <= prob:
                    self.model.event_history.append([self.id,obj,action_type,current_time])
			

    def parseAttribute(self, attr):
        pass
        # parse attributes returned by AnalysisLib.getAttributesOfUser()
