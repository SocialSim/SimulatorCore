from SimulatorCore.SimulatorCore import SimulatorCore
from AgentBuilder.AgentBuilder import AgentBuilder

def main():
    agentBuilder = AgentBuilder()
    agentList = agentBuilder.build()

    simulatorCore = SimulatorCore(agentList = agentList,
            startTime = 0,
            endTime = 24 * 10)
    simulatorCore.simulate()
    simulatorCore.showLog()


if __name__ == "__main__":
    main()

