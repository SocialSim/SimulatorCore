import Object.GithubChallenge.GithubRepository.GithubRepository as objectTemplate
from AnalysisLib.AnalysisLib import AnalysisLib
from Object.GithubChallenge.GithubRepository.GithubRepository import GithubRepository

from utils import utils

class ObjectBuilder():

    def __init__(self, attributeList):
        self.analysis_lib = AnalysisLib()
        self.objectList = list()
        self.attributeList = attributeList

    def build(self):
        self.createObjects()
        return self.objectList

    def createObjects(self):
        # ask for a list of user id
        self.object_id = self.analysis_lib.getListOfObjID()

        # for each user id, we instantiate a SimpleGithubAgent

        # Note: for now we assume agentID is integer. However, different social
        # media might choose different format of ID. mesa framework use integer
        # as unique_id
        for objId in self.object_id:
            obj = objectTemplate.GithubRepository(self.attributeList[utils.get_dict_id_index(objId, self.attributeList)])
            self.objectList.append({"id": objId, "obj": obj})

