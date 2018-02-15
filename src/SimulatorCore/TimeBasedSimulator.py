import random
import numpy as np


class TimeBasedSimulator():

    def __init__(self, agents, startTime, endTime, unitTime):
        self.agents = agents
        self.currentTime = startTime
        self.startTime = startTime
        self.endTime = endTime
        self.unitTime = unitTime
        self.eventHistory = []

        
    def run(self):
        for currentTime in np.arange(self.startTime, self.endTime, self.unitTime):
            for agent in self.agents:
                events = agent.step(currentTime)
            self.eventHistory += events

            
    def showLog(self):
        for event in self.eventHistory:
            print(event)

