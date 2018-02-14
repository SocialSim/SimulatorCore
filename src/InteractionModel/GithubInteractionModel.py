# agent action format: [self.id, obj, action_type, current_time]
from utils import utils

class GitHubInteractionModel():

    def __init__(self, agent_list, object_list):
        self.agent_list = agent_list
        self.object_list = object_list

    def update(self, action):
        if action[2] == "star":
            target_obj = self.object_list[utils.get_dict_id_index(action[1], self.object_list)]["obj"]
            target_obj.star(action[0], action[3])

        # insert other action_type event handlers

        return self.agent_list, self.object_list