class Agent(object):
    '''An abstract class for user and object agent models.'''

    def __init__(self, id):
        self.id = id
        pass

    def build(self):
        '''Query AnalysisLib to get model attributes.'''
        pass

    def step(self, currentTime, timeStep):
        '''
        The step() function is used by TimeBasedSimulator. This function is invoked at every time step in the simulation loop.

        :param currentTime: current simulation time
        :return: the list of instantaneous events the user generates at the given time.
        '''
        pass

    def next(self, currentTime, timeStep):
        '''
        The next() function is used by EventBasedSimulator.

        :param currentTime: current simulation time
        :return: the next event the user generates in the nearest future.
        '''
        pass

    def getID(self):
        '''
        The getID() function is used by evaluation engine.

        :return: the id of this agent
        '''
        return self.id
