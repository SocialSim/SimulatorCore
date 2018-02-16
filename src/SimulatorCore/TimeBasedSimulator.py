import random
import numpy as np
import json

class TimeBasedSimulator():

    def __init__(self, agents, objects, actions, startTime, endTime, unitTime):
        self.agents = agents            
        self.objects = objects
        self.actions = actions
        self.startTime = startTime
        self.endTime = endTime
        self.unitTime = unitTime
        self.actionHistory = []

        
    def simulate(self):
        for currentTime in np.arange(self.startTime, self.endTime, self.unitTime):
            self.step(currentTime)


    def step(self, currentTime):
        random.shuffle(self.agents)
        for agent in self.agents:
            actions = agent.step(currentTime)
            for action in actions:
                # given agent-generated action, update agents and objects based on interaction
                self.update(action)
                self.actionHistory.append(action)


    def update(self, action):
        for targetObject in self.objects:
            if targetObject.returnId() == action[1]:
                targetObject.updateAttributes(action[0], self.actions["object_attribute"][self.actions["action"].index(action[2])], action[3])
                break
        # include other types of interactions based on action definitions from the config file (later db)  

            
    def showLog(self):
        # show log of event history
        for i in range(len(self.actionHistory)):
            print(self.actionHistory[i])

        # show log of object attributes
        for i in range(len(self.objects)):
            attributes = self.objects[i].returnAttributes()
            print(json.dumps(attributes, indent=1))

        # show log of agent attributes
        for i in range(len(self.agents)):
            attributes = self.agents[i].returnAttributes()
            print(json.dumps(attributes, indent=1))
