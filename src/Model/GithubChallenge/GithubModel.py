from mesa import Agent, Model
from mesa.time import RandomActivation
import random

from Agent.GithubChallenge.SimpleGithubAgent.SimpleGithubAgent import SimpleGithubAgent
from Object.GithubChallenge.GithubRepository.GithubRepository import GithubRepository
from Model.Model import SocialSimModel

class GithubModel(SocialSimModel):

    """ Model for Github Challenge"""
    def __init__(self, numAgents, numObjects):
        self.num_agents = N
        self.num_objects = N

        self.schedule = RandomActivation(self)
    
        # creating behavior models

        # creating agents

        # creating repositories


    def step(self):
        self.schedule.step()

    def createAgents(self):
        createGithubAgents()

    def createObjects(self):
        createGithubObjects()

    def createBehaviorModel(self):
        pass

#####

    def createGithubAgents(self):
        for i in range(self.num_agents):
            a = SimpleGithubAgent(i, self)
            self.schedule.add(a)

    def createGithubObjects(self):
        pass

