from mesa import Agent, Model
from mesa.time import RandomActivation
import random

from Agent.GithubChallenge.SimpleGithubAgent.SimpleGithubAgent import SimpleGithubAgent
from Object.GithubChallenge.GithubRepository.GithubRepository import GithubRepository
from Model.Model import SocialSimModel
from AnalysisLib.AnalysisLib import AnalysisLib

class GithubModel(SocialSimModel):

    """ Model for Github Challenge"""
    def __init__(self):

        self.schedule = RandomActivation(self)

        self.analysis_lib = AnalysisLib()
    
        # creating behavior models

        # creating agents
        self.createAgents()

        # creating repositories
        self.createObjects()

        # Note: assume for now the time granularity is 1 hour. (Consistent with
        # data from datacube)
        self.current_time = 0

    def step(self):
        self.schedule.step()
        self.current_time = (self.current_time + 1) % 24

    def createAgents(self):
        createGithubAgents()

    def createObjects(self):
        createGithubObjects()

    def createBehaviorModel(self):
        pass

#####

    def createGithubAgents(self):

        # ask for a list of user id
        self.agent_id = self.analysis_lib.getListOfAgentID()
        self.num_agents = len(self.agent_id)

        # for each user id, we instantiate a SimpleGithubAgent
        # ask for the probability for this agent and initialize it

        # Note: for now we assume agentID is integer. However, different social
        # media might choose different format of ID. mesa framework use integer
        # as unique_id
        for agentId in self.agent_id:
            ind_prob = self.analysis_lib.getIndendentProbOfAgent(agentId)
            agent = SimpleGithubAgent(agentId, self, ind_prob)
            # Note: need to ask for other needed attributes and parse them
            self.schedule.add(agent)

    def createGithubObjects(self):
        # ask for a list of object id
        self.obj_id = self.analysis_lib.getListOfObjID()
        self.num_objs = len(self.obj_id)

        # for each obj id, we instantiate a GithubRepository 
        # ask for attributes and initilize them. Put them in a dictionary
        for objId in self.obj_id:
            # Note: need to ask for other needed attributes and parse them and instantiate them
            return


