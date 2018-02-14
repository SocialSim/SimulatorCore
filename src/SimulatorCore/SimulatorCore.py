class SimulatorCore():

    def __init__(self, agentList, objectList, interactionModel, startTime, endTime):
        self.agentList = agentList
        self.objectList = objectList
        self.interactionModel = interactionModel
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
                self.agentList, self.objectList = self.interactionModel.update(action)
                self.eventHistory.append(action)

        self.currentTime = self.currentTime + 1

    def showLog(self):
        # show log of event history
        for i in range(len(self.eventHistory)):
            print(self.eventHistory[i])

        # show log of object attributes
        for i in range(len(self.objectList)):
            print(self.objectList[i]["obj"].returnAttributes())

        # show log of agent attributes
        for i in range(len(self.agentList)):
            print(self.agentList[i].returnAttributes())