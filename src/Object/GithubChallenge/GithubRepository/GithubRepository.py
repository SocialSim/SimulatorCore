class Object(object):

    ''' Init function '''
    def __init__(self, unique_id, analysis_lib, attributes):
        self.id = unique_id
        self.analysisLib = analysis_lib
        self.attributes = attributes

    def returnAttributes(self):
        return self.attributes

    def returnId(self):
        return self.id

    def updateAttributes(self, actorId, action, timestamp):
        self.attributes[action].append({"id": actorId, "timestamp": timestamp})
        pass
