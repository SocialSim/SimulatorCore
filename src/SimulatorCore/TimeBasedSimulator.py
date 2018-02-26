import random
import numpy as np
from DependencyLogger.DependencyLogger import DependencyLogger


class TimeBasedSimulator():
    '''
    A simple implementation of a time-based simulator. The core of the simulation is a loop that advances simulation time in uniform time step. Within the loop, the simulator first
    - shuffles the list of user agents, then
    - for each user agent in the list, calls the agent's step() function. 
    Time unit: hour
    '''

    def __init__(self, userAgents, objectAgents, startTime, endTime, unitTime):
        self.userAgents = userAgents
        self.objectAgents = objectAgents
        self.currentTime = startTime
        self.startTime = startTime
        self.endTime = endTime
        self.unitTime = unitTime
        self.eventHistory = []

        self.dependencyLogger = DependencyLogger(10, self.startTime, self.unitTime)

    def run(self):
        for currentTime in np.arange(self.startTime, self.endTime,
                                     self.unitTime):
            self.step(currentTime)

    def step(self, currentTime):
        random.shuffle(self.userAgents)
        self.dependencyLogger.step()

        for agent in self.userAgents:
            events = agent.step(currentTime, self.unitTime)
            self.eventHistory += events

    def showLog(self):
        for event in self.eventHistory:
            print(event)

    def getCurrentTime(self):
        return self.currentTime
