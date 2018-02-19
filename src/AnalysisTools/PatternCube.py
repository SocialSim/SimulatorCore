from collections import OrderedDict

import json

class pattern_cube:

    def __init__(self):
        # load test probabilities
        # NOTE: These probabilities are derived from real-world GitHub PushEvent data and are discretized using KSC
        self.probabilities = self.load_probabilities()
        self.default_dist = [0,0,0,0,0,0,0,0,0,0.2,0.1,0.1,0.2,0.1,0.1,0.1,0.1,0.0,0.0,0,0,0,0,0]
    
    def get_independent_probability(self, actor, receiver, action):
        if action == "push":
            return self.query(self.cluster(actor, "agent", action), self.cluster(receiver, "object", action), action)
        else:
            return self.default_dist

    # Query post-processing table in db containing probability distribution
    # Actual pattern cube iterates through aggregate tables and builds distributions
    def query(self, actor, receiver, action):
        # SELECT * FROM pattern_cube WHERE actor = 1 AND receiver = 1 AND action = "PushEvent"
        return self.probabilities[actor + receiver]["distribution"]

         
    # Cluster propagator and reciever types based on attributes
    # Supposed to cluster based on action definition. ie agent-on-agent singular, agent-on-object multiple
    # Supposed to be high-dimensional K-means defined by Hartigan Index
    def cluster(self, attributes, actor_type, action):
        if actor_type == "agent":
            if attributes["followers"] >= 100:
                return "a1"
            elif attributes["followers"] < 100 and attributes["followers"] >= 10:
                return "a2"
            else:
                return "a3"
        else: # if "object
            if attributes["language"] == "JavaScript":
                return "r1"
            else: # if "Python"
                return "r2"

    # Roll-up or drill-down on given axis
    def change_granularity(self, scale, axis):
        pass    

    # Load in probabilities as placeholders for database and SQL queries
    def load_probabilities(self):
        with open("../config/push_probability.json") as data_file:
            data = json.load(data_file, object_pairs_hook=OrderedDict)
        return data