from Agent.Agent import Agent


class SimpleObjectAgent(Agent):
    '''
    A simple Github object agent model.
    TODO complete the class functions
    '''
    
    def __init__(self, id):
        super(SimpleObjectAgent, self).__init__(id)

        # Populate user attribute with data
        self.build()


    def build(self):
        pass

    def step(self, currentTime, timeStep):
        pass

    def next(self, currentTime, timeStep):
        pass
