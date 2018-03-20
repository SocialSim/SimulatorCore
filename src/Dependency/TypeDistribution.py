class TypeDistribution():
    '''
    A simple data structure to hold an agent's action rate each hour of a day. This time-dependent action is independent of other agents' actions.

    eventTypes = {"CommitCommentEvent": 0, "CreateEvent": 1, "DeleteEvent": 2, "ForkEvent": 3,
                           "IssueCommentEvent": 4, "IssuesEvent": 5, "PullRequestEvent": 6, "PushEvent": 7,
                           "WatchEvent": 8, "PublicEvent": 9, "MemberEvent": 10, "GollumEvent": 11,
                           "ReleaseEvent": 12, "PullRequestReviewCommentEvent": 13}
    '''

    def __init__(self, agentId, probs):
        '''
        Data sturucure for user's type-specific hourly action distribution.
        :param agentId: user Id
        :param probs: probability distribution over different action types
        '''
        self.agentId = agentId
        self.probs = list(probs)

        # Make sure probs is a proper distribution
        assert (round(sum(probs), 6), 1.0)
        assert (all(0.0 <= prob <= 1.0 for prob in probs))
        assert (len(probs) == 14)

    def __str__(self):
        return "{%s %s}" % (str(self.agentId), str(self.probs))

    def getAgentId(self):
        return self.agentId

    def getProbs(self):
        return self.probs

def TypeDistributionSerializer(obj):
    if isinstance(obj, TypeDistribution):
        serial = str(obj)
        return serial
    else:
        raise TypeError ("Type not serializable")
