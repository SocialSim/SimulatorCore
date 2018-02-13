import random

class SimulatorCore():

    def __init__(self, agentList, startTime, endTime):
        self.agentList = agentList
        self.currentTime = startTime
        self.startTime = startTime
        self.endTime = endTime
        self.eventHistory = []

    def simulate(self):
        for i in range(self.startTime, self.endTime):
            self.step()

    def step(self):
        for agent in self.agentList:
            action_list = agent.step(self.currentTime)
            for action in action_list:
                self.eventHistory.append(action)

        self.currentTime = self.currentTime + 1

    def showLog(self):
        for i in range(len(self.eventHistory)):
            print(self.eventHistory[i])

