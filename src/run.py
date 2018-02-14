from SimulatorCore.SimulatorCore import SimulatorCore
from AgentBuilder.AgentBuilder import AgentBuilder
from ObjectBuilder.ObjectBuilder import ObjectBuilder
from InteractionModel.GithubInteractionModel import GitHubInteractionModel

from utils import utils

# run simulation
def main():
    # load initial agent/object attributes from config file that will be generated from database
    config = utils.get_attributes()

    agentBuilder = AgentBuilder(config["agents"]["attributes"])
    agentList = agentBuilder.build()

    objectBuilder = ObjectBuilder(config["objects"]["attributes"])
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

