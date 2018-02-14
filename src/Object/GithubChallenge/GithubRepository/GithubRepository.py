class GithubRepository(object):

    def __init__(self, attributes):
        pass
        # initialize any attributes
        # logs
        # do we do a register-notification based log or just any log?
        self.attributes = attributes

    def updateLog(self, log):
        pass
        # log should be a Log class type

    def push(self):
        pass

    def pull(self):
        pass

    def star(self, agentId, step):
        self.attributes["stars"].append({"id": agentId, "step": step})

    def issue(self):
        pass

    def returnAttributes(self):
        return self.attributes

