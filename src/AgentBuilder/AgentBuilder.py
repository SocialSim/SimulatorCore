import Agent.GithubChallenge.SimpleGithubAgent as SimpleGithubAgent
from AnalysisLib.AnalysisLib import AnalysisLib


class AgentBuilder():
    '''
    This class is responsible for building agent objects from AnalysisLib. For now, each user in the database is modeled by one separate agent object. FUTURE IMPROVEMENT: users with homogenous behaviors are grouped into a single generic agent object. For example, one generic agent object handles all users who perform only 1 to 3 actions per months.
    '''

    def __init__(self, AgentModel=SimpleGithubAgent):
        '''
        Initialize the AgentBuilder

        :param AgentModel: the class of agent used to construct agent objects, which is passed down from the main() function.
        '''

        self.AgentModel = AgentModel

    
    def build(self):
        '''
        Build a list of agents for the simulator. Each user in the database is modeled by one separate agent object.

        :return: a list of agents
        '''
        
        # Ask AnalysisLib for a list of agent IDs
        agentIds = AnalysisLib.getListOfAgentIds()
        agents = []
        
        for agentId in agentIds:
            # Note: for now we assume agentID is integer. However, different social
            # media might choose different format of ID. mesa framework use integer
            # as unique_id

            # Instantiate new agent object of class AgentModel
            # TODO configure agent model like setting top-k influential users + activity
            agent = self.AgentModel.Agent(agentId)

            agents.append(agent)

        return agents

