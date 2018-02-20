import random
import numpy as np


class TimeBasedSimulator():
    '''
    A simple implementation of a time-based simulator. The core of the simulation is a loop that advances simulation time in uniform time step. Within the loop, the simulator shuffles the agent list and thencalls each agent in the list to perform its action. 
    Time unit: hour
    '''

    def __init__(self, agents, startTime, endTime, unitTime):
        self.agents = agents
        self.currentTime = startTime
        self.startTime = startTime
        self.endTime = endTime
        self.unitTime = unitTime
        self.eventHistory = []

    def run(self):
        for currentTime in np.arange(self.startTime, self.endTime,
                                     self.unitTime):
            random.shuffle(self.agents)
            for agent in self.agents:
                events = agent.step(currentTime, self.unitTime)
                self.eventHistory += events

    def showLog(self):
        for event in self.eventHistory:
            print(event)
