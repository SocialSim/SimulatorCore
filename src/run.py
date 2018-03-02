from SimulatorCore.TimeBasedSimulator import TimeBasedSimulator
from AgentBuilder.AgentBuilder import AgentBuilder
from Agent.GithubChallenge.SimpleUserAgent import SimpleUserAgent
from Agent.GithubChallenge.SimpleObjectAgent import SimpleObjectAgent


def main():
    # Init and config AgentBuilder
    agentBuilder = AgentBuilder(UserAgentModel=SimpleUserAgent,
                                ObjectAgentModel=SimpleObjectAgent)
    userAgents, objectAgents = agentBuilder.build()

    # Init and config simulation setting
    simulator = TimeBasedSimulator( userAgents=userAgents,
                                    objectAgents=objectAgents,
                                    startTime=0, endTime=24, unitTime=1)
    simulator.run()
    simulator.showLog()

    # TODO collect data and analyze


if __name__ == "__main__":
    main()
