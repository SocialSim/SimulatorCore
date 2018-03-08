class UserDependency():
    '''
    A simple data structure to hold an agent's dependency over other related users.
    '''

    def __init__(self, userId, userDependency):
        self.userId = userId
        self.depUserIds = list(userDependency.keys())
        self.userDependency = userDependency

        assert (all(0.0 <= depProb <= 1.0 for depProb in userDependency.values()))

    def __str__(self):
        return "{%s %s %s}" % (str(self.userId), str(self.depUserIds), 
                str(self.userDependency))

def UserDependencySerializer(obj):
    if isinstance(obj, UserDependency):
        serial = str(obj)
        return serial
    else:
        raise TypeError ("Type not serializable")
