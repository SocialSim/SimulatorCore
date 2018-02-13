import random

class BernoulliModel(object):

    def __init__(self):
        pass

    def predict_obj(self, obj_id, event_type):
        for action_type in obj:
            prob = action_type.get_prob_at()
            if random.random() <= prob:

