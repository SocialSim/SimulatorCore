from common.const import *

class DependencyLogger:
    ''' DependencyLogger keeps track of past events of some user Agents.

    This module is an alias to DependencyManager. Its functionality is to
    provide an in memory look up table for events executed by some user agents
    in the past few ticks. Current implementation of DependencyLogger is a
    ring buffer style two dimensional array.

    Note:
        step() interface should be invoked in each simulation tick before any
        other agents are simulated.

    Attributes:
        logDepth(int): the depth of look up table. DependencyLogger will only
        remember events up to past logDepth ticks.
        currTime(int): current time of the simulation. This value should be
        consistent with the one in CoreSimulator.
        head(int): head pointer for ring buffer. Its position dictates the next
        slot in log that should store the event.
        log(dict): the place where logs are stored. It is a map from userID to
        a list of set, where each set stores all the events that are performed
        by a particular agent at that timestamp

    '''
    _instance = None

    @staticmethod
    def getInstance(logDepth = 10, startTime = 0, unitTime = 1):
        """ Static access method. """
        if DependencyLogger._instance is None:
            DependencyLogger(logDepth, startTime, unitTime)
        return DependencyLogger._instance

    def __init__(self, logDepth = 10, startTime = 0, unitTime = 1):
        ''' initialize DependencyLogger with its logDepth and startTime

        Note: currentTime and head are initialized with a -1. This is because
        we assume step() function will be invoked before any other agents are
        simulated. Therefore when the first time step() is invoked, they will
        be set to the right start values.

        Args:
            logDepth(int): parameter to initialize self.logDepth
            startTime(int): parameter to intialize startTime

        '''
        if DependencyLogger._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DependencyLogger._instance = self

        self.logDepth = logDepth
        self.currTime = startTime - 1
        self.unitTime = unitTime
        self.head = -1
        self.log = dict()


    def initLoggerFromDataset(self, logs):
        ''' initialize DependencyLogger internals with data from dataset.

        Args:
            logs(list): logs that are used to initialize DependencyLogger. Its
            internal reprensentation should be [[userID, eventType, ts]...]

        '''

        for log in logs:
            userID = log[DEPENDENCY_USER]
            eventType = log[DEPENDENCY_EVENT]
            timestamp = log[DEPENDENCY_TIMESTAMP]
            self.logUserEventAtTime(userID, eventType, timestamp)


    def checkUserEventAtTime(self, userID, eventType, timestamp):
        ''' Check if userID has performed eventType at timestamp.

        Args:
            userID(int): target user ID.
            eventType(application specific): target event type.
            timestamp(int): should be a past time stamp.

        Returns:
            True if userID has performed eventType at timestamp. False otherwise.

        Raises:
            Exception: this function will raise exception when some user agent
            tries to log event that is in future, or log events that are beyond
            logDepth.

        '''
        # User agent cannot log event that is too old
        if timestamp <= self.currTime - self.logDepth:
            raise Exception("Bam! You are spoiling my memory!")

        if timestamp > self.currTime:
            raise Exception("I do not remember event in the future")

        if userID not in self.log:
            return False

        timeDelta = self.currTime - timestamp
        if eventType not in self.log[userID][self.head - timeDelta]:
            return False

        return True


    def logUserEventAtTime(self, userID, eventType, timestamp):
        ''' log an event

        Args:
            userID(int): target user ID.
            eventType(application specific): target event type.
            timestamp(int): should be a past time stamp.

        Raises:
            Exception: this function will raise exception when some user agent
            tries to log event that is in future, or log events that are beyond
            logDepth.

        '''
        # User agent cannot log event that is too old
        if timestamp <= self.currTime - self.logDepth:
            raise Exception("Bam! You are spoiling my memory!")

        if timestamp > self.currTime:
            raise Exception("I do not remember event in the future")

        if userID not in self.log:
            self.log[userID] = [set()for i in range(0, self.logDepth)]
        timeDelta = self.currTime - timestamp
        self.log[userID][self.head - timeDelta].add(eventType)


    def step(self):
        ''' refresh internal variables through each tick.

        '''
        self.head += 1
        self.currTime += self.unitTime
        for _, userLog in self.log.iteritems():
            userLog[self.currTime % self.logDepth].clear()



if __name__ == "__main__":
    dl = DependencyLogger(10)
    eventLogs = list()
    eventLogs.append([12, "PushEvent", -2])
    eventLogs.append([3, "PullEvent", -1])
    dl.initLoggerFromDataset(eventLogs)
    dl.step()
    dl.logUserEventAtTime(1, "PullEvent", 0)
    dl.logUserEventAtTime(1, "PushEvent", 0)
    print (dl.log)
    print (dl.checkUserEventAtTime(1, "PullEvent", 0))
    print (dl.checkUserEventAtTime(1, "PushEvent", -1))
