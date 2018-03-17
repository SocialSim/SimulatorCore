### Directory Structure
This section describes directory structure of this repository

### Implement new social community
When implementing new social community, among all the components described in the architecture
- __Agent Model__ is required to reimplemented completely. New Agent Model is required to store any attributes that are pertinent to simulation.
- __Agent Builder__ is required to be modified such that it instantiates new Agent Model

### Interface
##### Agent Model:
- __init__: it is mandatory to pass the first argument as an unique ID (community dependent) and second argument as an instance of analysis library. It is up to developer to add more arguments after them.
- __step__: only used in time based simulation. It is invoked each step by Simulator Core.

##### Analysis Library:
- __init__: initialize the length of dependency time as one hour. Initialize activity threshold when activities over this threshold will be counted as active users. Set the denpendency threshold when the conditional probability over this threshold. Initialize a queue unsing list-like container to represent events. Initialize lists of user ids and object ids. Set the event types (currently for events in GitHub). Initialize user object preference, user hourly action rate, user total action count, and user dependencies as dictionaries. Initialize count for each type actions and object preference as dictionaries. Initialize general hourly action rate as hourly distributions for each type with an zero numpy array with length 24 (hour).
- __firstPass__: 
