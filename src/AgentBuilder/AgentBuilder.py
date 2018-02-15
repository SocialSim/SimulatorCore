import Agent.GithubChallenge.SimpleGithubAgent as SimpleGithubAgent
from AnalysisLib.AnalysisLib import AnalysisLib


class AgentBuilder():
    '''This class is responsible for building agents from AnalysisLib. For now, each user in the database is modeled by one agent object. In the future, nonactive users, say, those who perform 1 to 3 actions per months, are grouped into a single generic agent object.'''

    def __init__(self, AgentModel=SimpleGithubAgent):
        self.AgentModel = AgentModel

    
    def build(self):
        '''Build and return a list of agents for the simulator.'''
        
        # Ask AnalysisLib for a list of agent IDs
        agentIds = AnalysisLib.getListOfAgentIds()
        agents = []
        
        for agentId in agentIds:
            # Note: for now we assume agentID is integer. However, different social
            # media might choose different format of ID. mesa framework use integer
            # as unique_id

            # Instantiate new agent object
            agent = self.AgentModel.Agent(agentId)
            # TODO: configure agent model like setting top-k influential users + activity            
            agents.append(agent)

        return agents

