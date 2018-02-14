import Agent.GithubChallenge.SimpleGithubAgent.SimpleGithubAgent as agentTemplate
from Object.GithubChallenge.GithubRepository.GithubRepository import GithubRepository

from utils import utils

class AgentBuilder():

    def __init__(self, attributeList, analysisLib):
        self.analysis_lib = analysisLib
        self.agentList = list()
        self.attributeList = attributeList

    def build(self):
        self.createAgents()
        return self.agentList

    def createAgents(self):
        # ask for a list of user id
        self.agent_id = self.analysis_lib.getIds("agents")

        # for each user id, we instantiate a SimpleGithubAgent

        # Note: for now we assume agentID is integer. However, different social
        # media might choose different format of ID. mesa framework use integer
        # as unique_id
        for agentId in self.agent_id:
            agent = agentTemplate.Agent(agentId, self.analysis_lib, self.attributeList[utils.get_dict_id_index(agentId, self.attributeList)])
            self.agentList.append(agent)

