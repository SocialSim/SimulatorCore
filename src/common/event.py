class Event(object):
    def __init__(self, userID, objID, eventType, timestamp):
        self.userID = userID
        self.objID = objID
        self.eventType = eventType
        self.timestamp = timestamp

    def getUserID(self):
        return self.userID

    def getObjID(self):
        return self.objID

    def getEventType(self):
        return self.eventType

    def getTimestamp(self):
        return self.timestamp

    def show(self):
        event = "userID: " + str(self.userID) +\
                ", objID: " + str(self.objID) +\
                ", eventType: " + self.eventType +\
                ", timestamp: " + str(self.timestamp)
        return event

    def eventLog(self):
        event = str(self.timestamp) + " " + str(self.userID) + " " + str(self.objID) + " " + self.eventType  + "\n"
        return event