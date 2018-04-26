import random
from common.const import *
from DependentEventLogger.DependentEventLogger import DependentEventLogger
from common.event import Event


class TimeBasedSimulator():
    '''
    A simple implementation of a time-based simulator. The core of the simulation is a loop that advances simulation time in uniform time step. Within the loop, the simulator first
    - shuffles the list of user agents, then
    - for each user agent in the list, calls the agent's step() function. 
    Time unit: hour
    '''

    def __init__(self, userAgents, objectAgents, temporalPreference, startTime, endTime, unitTime):
        self.userAgents = userAgents
        self.objectAgents = objectAgents
        self.temporalPreference = temporalPreference
        self.currentTime = startTime
        self.startTime = startTime
        self.endTime = endTime
        self.unitTime = unitTime
        self.eventHistory = []
        self.runWithTemporalPreference = False # Set True to enable temporal preference agent clustering
        self.dependentEventLogger = DependentEventLogger.getInstance(100, self.startTime, self.unitTime)

    def run(self):
        if (self.runWithTemporalPreference):
            print("NOTE: Running with temporal preference enabled")

        while self.currentTime < self.endTime:
            print("Timestemp:", self.currentTime)
            if (self.runWithTemporalPreference):
                self.stepWithTemporalPreference()
            else:
                self.step()
            self.currentTime += self.unitTime

    def stepWithTemporalPreference(self):
        self.dependentEventLogger.step()

        userTempDist = self.temporalPreference[self.currentTime]
        for i in userTempDist:
            agent = self.userAgents[i]
            events = agent.step(self.currentTime, self.unitTime)
            self.logEvents(events)
            self.eventHistory += events

    def step(self):
        self.dependentEventLogger.step()

        for agent in self.userAgents:
            events = agent.step(self.currentTime, self.unitTime)
            self.logEvents(events)
            self.eventHistory += events

    def logEvents(self, events):
        for event in events:
            userId = event.getUserID()
            eventType = event.getEventType()
            timeStamp = event.getTimestamp()
            self.dependentEventLogger.logUserEventAtTime(userID = userId,
                    eventType = eventType,
                    timestamp = timeStamp)

    def showLog(self):
        for event in self.eventHistory:
            print(event.show())

    def saveLog(self):
        fname = "text.txt"
        if (self.runWithTemporalPreference):
            fname = "temp_pref.txt"
        else:
            fname = "no_temp_pref.txt"

        f = open(LOG_OUTPUT + fname, "w")
        for event in self.eventHistory: 
            f.write(event.eventLog())
        f.close()

    def getCurrentTime(self):
        return self.currentTime

    def getAllUserIDs(self):
        ids = list()
        for agent in self.userAgents:
            ids.append(agent.getID())
        return ids
        
