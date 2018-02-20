from SimulatorCore.TimeBasedSimulator import TimeBasedSimulator
from AgentBuilder.AgentBuilder import AgentBuilder
import Agent.GithubChallenge.SimpleGithubAgent as SimpleGithubAgent


def main():
    # Init and config AgentBuilder
    agentBuilder = AgentBuilder(AgentModel=SimpleGithubAgent)
    agents = agentBuilder.build()

    # TODO init and config Dependency Manager

    # Init and config simulation setting
    simulator = TimeBasedSimulator(
        agents=agents, startTime=0, endTime=24, unitTime=1)
    simulator.run()
    simulator.showLog()

    # TODO collect data and analyze


if __name__ == "__main__":
    main()
