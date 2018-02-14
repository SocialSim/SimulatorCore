## SocialCube - A Multiscale Modeling and Simulation Framework for Social Streams

#### Overview
This repository contains framework code for SocialCube, a multiscale modeling and simulation framework for social streams.

#### Architecture
The following diagram shows a high level architecture of the framework.
![Arch](arch.png)

* __SimulatorCore__: there are time based simulator core and event based simulator core. Current implementation only contains event based simulator core for fast development and experiment.
* __Agent Builder__: responsible for getting a list of agent ids, and initializing each agent based on a specific agent model and provided initial attributes.
* __Object Builder__: responsible for getting a list of object ids, and initializing each object based on provided initial attributes.
* __Agent Model__: an agent class that describes user of certain social community.
* __Object Model__: an object class that describes agent-generated objects.
* __Interaction Model__: this describes the types of action/reaction scenarios of an agent action at any given timestep. The models are medium-specific, but can be easily switched out.
* __Behavior Model__: describes "personality" of an agent. Technically, it describes how an agent should behave given certain probability.
* __Dependency Manager__: responsible for updating simulated action into database, and querying past history of agents. It is only used when behavior model take dependent relationship into account.
* __Analysis Library__: responsible for analyzing dataset and building initial statistics and probability.

#### Agent & Object Configurations
The `~/config/config.json` file contains the initial agent- and object-specific attributes for a given simulation run, as well as available action types. This can be user-defined or generated from the database.

#### Setup
Follow these steps when setup in Debian based OS:
```
$ bash setup.sh
$ source ~/.profile
```
