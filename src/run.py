from SimulatorCore.TimeBasedSimulator import TimeBasedSimulator
from AgentBuilder.AgentBuilder import AgentBuilder


def main():
    # Init and config AgentBuilder
    agentBuilder = AgentBuilder()
    agents = agentBuilder.build()

    # Init and config simulation setting
    simulator = TimeBasedSimulator(agents=agents, startTime=0, endTime=24*10, unitTime=1)
    simulator.run()
    simulator.showLog()

    # TODO: collect data and analyze

    
if __name__ == "__main__":
    main()

