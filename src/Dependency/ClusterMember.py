class ClusterMember():
    '''
    A simple data structure to hold an agent's action distribution among different event types.
    '''

    def __init__(self, clusterId, members):

        self.clusterId = clusterId
        self.members = members


    def __str__(self):
        return "{%s %s}" % (str(self.clusterId), str(self.members))

    def getClusterId(self):
        return self.clusterId

    def getMembers(self):
        return self.members

def ClusterMemberSerializer(obj):
    if isinstance(obj, ClusterMember):
        serial = str(obj)
        return serial
    else:
        raise TypeError ("Type not serializable")