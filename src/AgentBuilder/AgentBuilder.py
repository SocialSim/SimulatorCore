from StatProxy.StatProxy import StatProxy
from Agent.GithubChallenge.SimpleUserAgent import SimpleUserAgent
from Agent.GithubChallenge.DependentUserAgent import DependentUserAgent


class AgentBuilder():
    '''
    This class is responsible for building agent objects using StatProxy. For now, each user in the database is modeled by one separate agent instance. FUTURE IMPROVEMENT: users with homogenous behaviors are grouped into a single generic agent instance. For example, one generic agent class to handle all users who perform only 1 to 3 actions per months.
    '''

    def __init__(self, UserAgentModel=None, ObjectAgentModel=None):
        '''
        :param UserAgentModel: the class of user agent to construct user agent instances, configured from the main() function.
        :param ObjectAgentModel: the class of object agent to construct object agent instances, configured from the main() function.
        '''

        self.UserAgentModel = UserAgentModel
        self.ObjectAgentModel = ObjectAgentModel
        if UserAgentModel == SimpleUserAgent:
            self.statProxy = StatProxy.getInstance(agentType="simple")
        else:
            self.statProxy = StatProxy.getInstance(agentType="dependent")


    def build(self):
        '''
        Build a list of user and object agent instances for the simulator. Each user in the original dataset is modeled by one separate user agent instance.

        :return: a list of user agents and a list of object agents
        '''

        # Ask StatProxy for a list of user IDs
        userIds = self.statProxy.getUserIds()
        userAgents = []
        
        for userId in userIds:
            # Note: for now we assume user ID is integer. However, different social
            # media might choose different format of ID.

            # Instantiate new user agent instance of class UserAgentModel
            # TODO configure user agent model like setting top-k influential users + activity
            # TODO configure user behavior model
            userAgent = self.UserAgentModel(userId)
            userAgents.append(userAgent)

        # Ask StatProxy for a list of object IDs
        objectIds = self.statProxy.getObjectIds() #getObjectIds()
        objectAgents = []

        for objectId in objectIds:
            objectAgent = self.ObjectAgentModel(objectId)
            objectAgents.append(objectAgent)
        
        return userAgents, objectAgents
