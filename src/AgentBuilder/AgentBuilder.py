import Agent.GithubChallenge.SimpleGithubAgent.SimpleGithubAgent as agentTemplate
from AnalysisLib.AnalysisLib import AnalysisLib
from Object.GithubChallenge.GithubRepository.GithubRepository import GithubRepository

class AgentBuilder():

    def __init__(self):
        self.analysis_lib = AnalysisLib()
        self.agentList = list()

    def build(self):
        self.createAgents()
        return self.agentList

    def createAgents(self):
        # ask for a list of user id
        self.agent_id = self.analysis_lib.getListOfAgentID()

        # for each user id, we instantiate a SimpleGithubAgent

        # Note: for now we assume agentID is integer. However, different social
        # media might choose different format of ID. mesa framework use integer
        # as unique_id
        for agentId in self.agent_id:
            agent = agentTemplate.Agent(agentId, self.analysis_lib)
            self.agentList.append(agent)

