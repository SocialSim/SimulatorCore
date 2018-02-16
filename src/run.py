from SimulatorCore.SimulatorCore import SimulatorCore
from AgentBuilder.AgentBuilder import AgentBuilder
from AnalysisLib.AnalysisLib import AnalysisLib

# run simulation
def main():
    # load initial agent/object attributes from config file that will be generated from database
    analysis_lib = AnalysisLib('../config/config.json')
    config = analysis_lib.getAttributes()

    agentBuilder = AgentBuilder(config["agents"]["attributes"], analysis_lib, "agents")
    agentList = agentBuilder.build()

    objectBuilder = AgentBuilder(config["objects"]["attributes"], analysis_lib, "objects")
    objectList = objectBuilder.build()

    simulatorCore = SimulatorCore(agentList = agentList,
            objectList = objectList,
            actions = analysis_lib.getActions(),
            startTime = 0,
            endTime = 24 * 10)
    simulatorCore.simulate()
    simulatorCore.showLog()


if __name__ == "__main__":
    main()

