from mesa import Agent
import random

class SimpleGithubAgent(Agent):

    ''' Init functino '''
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

    ''' Function to perform for every step'''
    def step(self):
        pass
        # For each interested repo
            # Flip a coin and see if I'm going to do any action on it

            # Flip a coin and see if I'm going to do any action based on others'
            # activity

    ''' Query DataCube on data it cares '''
    def queryCube(self):
        pass
        # Get top K1 influced users

        # Get top K2 repos I'm interested in

