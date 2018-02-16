import Agent.GithubChallenge.SimpleGithubAgent.SimpleGithubAgent as agentTemplate

from utils import utils

class AgentBuilder():

    def __init__(self, attribute_list, analysis_lib, class_type):
        self.analysis_lib = analysis_lib
        self.agent_list = list()
        self.attribute_list = attribute_list
        self.class_type = class_type

    def build(self):
        self.createAgents()
        return self.agent_list

    def createAgents(self):
        # ask for a list of user id
        self.agent_id = self.analysis_lib.getIds(self.class_type)

        # for each user id, we instantiate a SimpleGithubAgent

        # Note: for now we assume agentID is integer. However, different social
        # media might choose different format of ID. mesa framework use integer
        # as unique_id
        for agentId in self.agent_id:
            agent = agentTemplate.Agent(agentId, self.analysis_lib, self.attribute_list[utils.get_dict_id_index(agentId, self.attribute_list)])
            self.agent_list.append(agent)

