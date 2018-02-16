class SimulatorCore():

    def __init__(self, agentList, objectList, actions, startTime, endTime):
        self.agentList = agentList
        self.objectList = objectList
        self.actions = actions
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
                # given agent-generated action, update agents and objects based on interaction
                self.update(action)
                self.eventHistory.append(action)

        self.currentTime = self.currentTime + 1

    def update(self, action):
        for targetObject in self.objectList:
            if targetObject.returnId() == action[1]:
                targetObject.updateAttributes(action[0], self.actions["object_attribute"][self.actions["action"].index(action[2])], action[3])
                break


    def showLog(self):
        # show log of event history
        for i in range(len(self.eventHistory)):
            print(self.eventHistory[i])

        # show log of object attributes
        for i in range(len(self.objectList)):
            print(self.objectList[i].returnAttributes())

        # show log of agent attributes
        for i in range(len(self.agentList)):
            print(self.agentList[i].returnAttributes())