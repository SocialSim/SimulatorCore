from SimulatorCore.TimeBasedSimulator import TimeBasedSimulator
from AgentBuilder.AgentBuilder import AgentBuilder
from AnalysisLib.AnalysisLib import AnalysisLib

# run simulation
def main():
    # load initial agent/object attributes from config file that will be generated from database
    analysis_lib = AnalysisLib('../config/config.json')
    config = analysis_lib.getAttributes()

    agentBuilder = AgentBuilder(
            attribute_list = config["agents"]["attributes"], 
            analysis_lib = analysis_lib,
            class_type = "agents")
    agentList = agentBuilder.build()

    objectBuilder = AgentBuilder(
            attribute_list = config["objects"]["attributes"], 
            analysis_lib = analysis_lib,
            class_type = "objects")
    objectList = objectBuilder.build()

    simulatorCore = TimeBasedSimulator(
            agents = agentList,
            objects = objectList,
            actions = analysis_lib.getActions(),
            startTime = 0,
            endTime = 24 * 10,
            unitTime = 1)
    simulatorCore.simulate()
    simulatorCore.showLog()

    # TODO collect data and analyze

    
if __name__ == "__main__":
    main()

