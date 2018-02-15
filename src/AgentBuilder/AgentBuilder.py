import Agent.GithubChallenge.SimpleGithubAgent.SimpleGithubAgent as SimpleGithubAgent
from AnalysisLib.AnalysisLib import AnalysisLib


class AgentBuilder():
    '''This class is responsible for building agents from AnalysisLib. For now, each user in the database is modeled by one agent object. In the future, nonactive users, say, those who perform 1 to 3 actions per months, are grouped into a single generic agent object.'''
    def __init__(self):
        # TODO: configure Agent Model, Behavior Model, model fidelity like top-k influential users + activity, and so on
        self.analysisLib = AnalysisLib()
        pass

    def build(self):
        '''Build and return a list of agents to be used by the simulation.'''
        
        # Ask AnalysisLib for a list of agent IDs
        agentIds = self.analysisLib.getListOfAgentIds()
        agents = []
        
        for agentId in agentIds:
            # Note: for now we assume agentID is integer. However, different social
            # media might choose different format of ID. mesa framework use integer
            # as unique_id

            # Instantiate new and blank agent object
            # The class of agent object is configured in __init__()
            # For the near future, just use SimpleGithubAgent
            agent = SimpleGithubAgent.Agent(agentId)

            # TODO: assign Behavior Model to agent
            # The Behavior Model is configured in __init__()

            # Populate the agent attribute with data
            # Future extension: customize agent.build() with build parameters
            agent.build()
            
            agents.append(agent)
            
        return agents

