from AnalysisLib.AnalysisLib import AnalysisLib


class AgentBuilder():
    '''
    This class is responsible for building agent objects using AnalysisLib. For now, each user in the database is modeled by one separate agent instance. FUTURE IMPROVEMENT: users with homogenous behaviors are grouped into a single generic agent instance. For example, one generic agent class to handle all users who perform only 1 to 3 actions per months.
    '''

    def __init__(self, AgentModel=None):
        '''
        :param AgentModel: the desired class of agent to construct agent instances, which is configured from the main() function.
        '''
        
        self.AgentModel = AgentModel

    
    def build(self):
        '''
        Build a list of agent instances for the simulator. Each user in the database is modeled by one separate agent instance.

        :return: a list of agents
        '''
        
        # Ask AnalysisLib for a list of agent IDs
        analysislib = AnalysisLib.getInstance()
        agentIds = analysislib.getListOfAgentIds()
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

