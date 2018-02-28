class UserDependency():
    '''
    A simple data structure to hold an agent's dependency over other related users.
    '''

    def __init__(self, userId, depUserIds, depUserProbs):
        self.userId = userId
        self.depUserIds = depUserIds
        self.depUserProbs = depUserProbs

        assert (len(depUserIds) == len(depUserProbs))
        assert (all(0.0 <= depProb <= 1.0 for depProb in depUserProbs))