from AnalysisLib.AnalysisLib import AnalysisLib
from Agent.GithubChallenge.SimpleGithubAgent.SimpleGithubAgent import Agent
from utils import utils

class AgentBuilder():
    '''
    This class is responsible for building agent objects from AnalysisLib. For now, each user in the database is modeled by one separate agent object. FUTURE IMPROVEMENT: users with homogenous behaviors are grouped into a single generic agent object. For example, one generic agent object handles all users who perform only 1 to 3 actions per months.
    '''

    def __init__(self, attribute_list = None, analysis_lib = None, class_type = None):
        '''
        Initialize the AgentBuilder

        :param AgentModel: the class of agent used to construct agent objects, which is passed down from the main() function.
        '''
        self.analysis_lib = analysis_lib
        self.agent_list = list()
        self.attribute_list = attribute_list
        self.class_type = class_type
        self.AgentModel = Agent

    
    def build(self):
        '''
        Build a list of agents for the simulator. Each user in the database is modeled by one separate agent object.

        :return: a list of agents
        '''
        
        self.createAgents()
        return self.agent_list


    def createAgents(self):
        # ask for a list of user id
        self.agent_id = self.analysis_lib.getIds(self.class_type)

        # Note: for now we assume agentID is integer. However, different social
        # media might choose different format of ID. mesa framework use integer
        # as unique_id
        for agentId in self.agent_id:
            agent = self.AgentModel(agentId, self.analysis_lib, self.attribute_list[utils.get_dict_id_index(agentId, self.attribute_list)])
            self.agent_list.append(agent)

