import random

from DependentEventLogger.DependentEventLogger import DependentEventLogger
from common.event import Event
from common.const import *
from common.simulationTime import SimulationTime


class TimeBasedSimulator():
    '''
    A simple implementation of a time-based simulator. The core of the simulation is a loop that advances simulation time in uniform time step. Within the loop, the simulator first
    - shuffles the list of user agents, then
    - for each user agent in the list, calls the agent's step() function. 
    Time unit: hour
    '''

    def __init__(self, userAgents, objectAgents, simulationLength, unitTime):
        self.userAgents = userAgents
        self.objectAgents = objectAgents
        self.simulationLength = simulationLength
        self.unitTime = unitTime
        self.eventHistory = []
        # self.dependentEventLogger = DependentEventLogger.getInstance(200, self.startTime, self.unitTime)

    def run(self):
        count = 0
        while count < self.simulationLength:
            self.step()
            count += 1
            if self.unitTime == "hour":
                SimulationTime.updateTime(hourShift=1)
            else:
                SimulationTime.updateTime(dayShift=1)

    def step(self):
        # random.shuffle(self.userAgents)
        # self.dependentEventLogger.step()

        for agent in self.userAgents:
            events = agent.step()
            # self.logEvents(events)
            self.eventHistory += events

    def logEvents(self, events):
        for event in events:
            userId = event.getUserID()
            eventType = event.getEventType()
            timeStamp = event.getEventTime()
            self.dependentEventLogger.logUserEventAtTime(userID = userId,
                    eventType = eventType,
                    timestamp = timeStamp)

    def showLog(self):
        for event in self.eventHistory:
            event.show()

    def saveLog(self):
        with open(DATAPATH+"simulated_events_2015-02-test.txt", "w") as output:
            for event in self.eventHistory:
                output.write(str(event.getEventTime()) + " " + str(event.getObjID()) + " " + str(event.getUserID())
                             + " " + str(event.getEventType()) + "\n")

    # def getCurrentTime(self):
    #     return self.currentTime

    def getAllUserIDs(self):
        ids = list()
        for agent in self.userAgents:
            ids.append(agent.getID())
        return ids
        
