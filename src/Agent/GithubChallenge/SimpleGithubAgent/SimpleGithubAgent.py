import random

# Note: right now, all the attrbutes of an agent should be passed from simulator during
# initialization. The reason behind this is that we want to minimize "point of
# contact" to analysis library for future maintanence. The other way to do it
# is that we only pass in agent_id, and initialize every other attribute as None.
# Then when github agent needs it, it then queries analysis library itself.
class Agent():

    ''' Init function '''
    def __init__(self, unique_id, analysis_lib, attributes):
        self.id = unique_id
        self.analysisLib = analysis_lib
        self.ind_prob = analysis_lib.getIndendentProbOfAgent(self.id)
        self.attributes = attributes
        # query for independent probability

    ''' Function to perform for every step'''
    # def step(self, current_time):
    #     action_list = list()

    #     # For each interested repository
    #     for obj in self.ind_prob.keys():
    #         # For each action type
    #         for action_type in self.ind_prob[obj]:
    #             prob = self.ind_prob[obj][action_type][current_time % 24]
    #             # Flip a coin and see if I'm going to do any action on it
    #             if random.random() <= prob:
    #                 if action_type == "star":
    #                     if obj not in self.attributes["stars"]:
    #                         self.attributes["stars"].append(obj)
    #                         action_list.append([self.id, obj, action_type, current_time])
    #                     else:
    #                         continue # this is not necessarily true
    #                 else:
    #                     action_list.append([self.id, obj, action_type, current_time])
    #                 break # the agent should only be able to take one action per time step

    #     return action_list
			
    def step(self, current_time):
        activity_history = list()

        object_list = self.analysisLib.getIds("objects")
        action_list = self.analysisLib.getActions()

        # For each interested repository
        for obj in object_list:
            # For each action type
            for action_type in action_list:
                prob = self.ind_prob[obj][action_type][current_time % 24]
                # Flip a coin and see if I'm going to do any action on it
                if random.random() <= prob:
                    if action_type == "star":
                        if obj not in self.attributes["stars"]:
                            self.attributes["stars"].append(obj)
                            activity_history.append([self.id, obj, action_type, current_time])
                        else:
                            continue # this is not necessarily true
                    else:
                        activity_history.append([self.id, obj, action_type, current_time])
                    break # the agent should only be able to take one action per time step

        return activity_history

    def parseAttribute(self, attr):
        pass
        # parse attributes returned by AnalysisLib.getAttributesOfUser()

    def returnAttributes(self):
        return self.attributes