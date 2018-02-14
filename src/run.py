from SimulatorCore.SimulatorCore import SimulatorCore
from AgentBuilder.AgentBuilder import AgentBuilder
from ObjectBuilder.ObjectBuilder import ObjectBuilder
from InteractionModel.GithubInteractionModel import GitHubInteractionModel
from AnalysisLib.AnalysisLib import AnalysisLib

# run simulation
def main():
    # load initial agent/object attributes from config file that will be generated from database
    analysis_lib = AnalysisLib('../config/config.json')
    config = analysis_lib.getAttributes()

    agentBuilder = AgentBuilder(config["agents"]["attributes"], analysis_lib)
    agentList = agentBuilder.build()

    objectBuilder = ObjectBuilder(config["objects"]["attributes"], analysis_lib)
    objectList = objectBuilder.build()

    interactionModel = GitHubInteractionModel(agentList, objectList)

    simulatorCore = SimulatorCore(agentList = agentList,
            objectList = objectList,
            interactionModel = interactionModel,
            startTime = 0,
            endTime = 24 * 10)
    simulatorCore.simulate()
    simulatorCore.showLog()


if __name__ == "__main__":
    main()

