import random

from DependentEventLogger.DependentEventLogger import DependentEventLogger


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
        self.dependentEventLogger = DependentEventLogger.getInstance(100, self.startTime, self.unitTime)

    def run(self):
        while self.currentTime < self.endTime:
            self.step()
            self.currentTime += self.unitTime

    def step(self):
        random.shuffle(self.userAgents)
        self.dependentEventLogger.step()

        for agent in self.userAgents:
            events = agent.step(self.currentTime, self.unitTime)
            #Log the simulated events
            for event in events:
                userId = event[0]
                eventType = event[2]
                timeStamp = event[3]
                self.dependentEventLogger.logUserEventAtTime(userId, eventType, timeStamp)
            self.eventHistory += events

    def showLog(self):
        for event in self.eventHistory:
            print(event)

    def getCurrentTime(self):
        return self.currentTime
