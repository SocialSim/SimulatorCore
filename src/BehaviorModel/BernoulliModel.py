import random
from Dependency.IndependentAction import IndependentAction


class BernoulliModel(object):

    def __init__(self):
        pass

    
    def evaluate(self, indAction):
        '''return True if the independent action will be performed, otherwise False.'''
        return random.random() <= indAction.prob
