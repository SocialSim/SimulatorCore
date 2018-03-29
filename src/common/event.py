class Event(object):
    def __init__(self, userID, objID, eventType, timestamp):
        self.userID = userID
        self.objID = objID
        self.eventType = eventType
        self.eventTime = timestamp

    def getUserID(self):
        return self.userID

    def getObjID(self):
        return self.objID

    def getEventType(self):
        return self.eventType

    def getEventTime(self):
        return self.eventTime

    def show(self):
        event = "userID: " + str(self.userID) +\
                ", objID: " + str(self.objID) +\
                ", eventType: " + self.eventType +\
                ", timestamp: " + str(self.eventTime)
        print event
