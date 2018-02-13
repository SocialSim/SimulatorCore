import random

# Note: right now, all the attrbutes of an agent should be passed from simulator during
# initialization. The reason behind this is that we want to minimize "point of
# contact" to analysis library for future maintanence. The other way to do it
# is that we only pass in agent_id, and initialize every other attribute as None.
# Then when github agent needs it, it then queries analysis library itself.
class Agent():

    ''' Init function '''
    def __init__(self, unique_id, analysis_lib):
        self.id = unique_id
        self.analysisLib = analysis_lib
        self.ind_prob = analysis_lib.getIndendentProbOfAgent(self.id)
        # query for independent probability

    ''' Function to perform for every step'''
    def step(self, current_time):
        action_list = list()

        # For each interested repository
        for obj in self.ind_prob.keys():
            # For each action type
            for action_type in self.ind_prob[obj]:
                prob = self.ind_prob[obj][action_type][current_time % 24]
                # Flip a coin and see if I'm going to do any action on it
                if random.random() <= prob:
                    action_list.append([self.id,obj,action_type,current_time])

        return action_list
			

    def parseAttribute(self, attr):
        pass
        # parse attributes returned by AnalysisLib.getAttributesOfUser()
