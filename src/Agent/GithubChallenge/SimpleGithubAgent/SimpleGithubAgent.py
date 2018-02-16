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
        self.attributes = attributes
        # query for independent probability

    ''' Function to perform for every step'''			
    def step(self, current_time):
        activity_history = list()

        object_list = self.analysisLib.getIds("objects")
        action_list = self.analysisLib.getActions()

        # For each interested repository
        for obj in object_list:
            # For each action type
            for i in range(len(action_list["action"])):
                prob = self.analysisLib.getIndendentProbOfAgent(self.id, obj, action_list["action"][i], current_time % 24)
                # Flip a coin and see if I'm going to do any action on it
                if random.random() <= prob:
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