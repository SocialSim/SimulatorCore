import random
from Dependency.IndependentAction import IndependentAction


class BernoulliModel():

    def __init__(self):
        pass


    @staticmethod
    def evaluate(indAction):
        '''
        Decide whether an action is to be performed by flipping a coin.

        :param indAction: agent's indepedent action
        :return: a Boolean variable, True if the action is performed and False otherwise.
        '''
        
        return random.random() <= indAction.prob
