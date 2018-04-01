from common.const import *
import numpy as np
from collections import deque
import copy
import time
import json
import sys
import pickle
import common.analysisArgParser as argParser
import matplotlib.pyplot as plt

from Dependency.ObjectPreference import ObjectPreference
from Dependency.HourlyActionRate import HourlyActionRate
from IndependentAnalysisLib import IndependentAnalysisLib


class TypeDependencyAnalysisLib(IndependentAnalysisLib):
    _instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if TypeDependencyAnalysisLib._instance is None:
            TypeDependencyAnalysisLib()
        return TypeDependencyAnalysisLib._instance

    def __init__(self , fileName = None):
        if TypeDependencyAnalysisLib._instance is not None:
            raise Exception("TypeDependencyAnalysisLib class is a singleton!")
        else:
            TypeDependencyAnalysisLib._instance = self

        super(TypeDependencyAnalysisLib, self).__init__(fileName)

        self.typeDenpendency = {}
        self.objectLastActionType = {}

        # Initialization
        self.initTypeDenpendency()
        self.initObjectLastActionType()

        # Find the overall type dependencies.
        self.typeDependencyPass()


    def initTypeDenpendency(self):
        '''
        Initialize the type dependency to be empty.
        :return:
        '''
        for leftType in CORE_EVENT_TYPES:
            self.typeDenpendency[leftType] = {}
            for rightType in CORE_EVENT_TYPES:
                self.typeDenpendency[leftType][rightType] = float(0)

    def initObjectLastActionType(self):
        '''
        Initialize the event type for the last action on each object.
        :return:
        '''
        for objectId in self.objectIds:
            if self.objectIds[objectId] > 2:
                self.objectLastActionType[objectId] = None

    def typeDependencyPass(self):
        '''
        This function will find the overall dependencies between consecutive actions on the same object.
        :return:
        '''
        with open(self.fileName, "r") as file:
            for line in file:
                if not line:
                    break
                else:
                    line = line.strip('\n')
                    eventTime, hour, objectId, userId, eventType = self.eventSplit(line)

                    # Skip the events types that we do not care.
                    if eventType not in self.coreEventTypes:
                        continue

                    if objectId in self.objectLastActionType:
                        if self.objectLastActionType[objectId]:
                            preEventType = self.objectLastActionType[objectId]
                            self.typeDenpendency[preEventType][eventType] += 1
                        self.objectLastActionType[objectId] = eventType

        # Summarize the type dependency
        for eventType in CORE_EVENT_TYPES:
            typeCount = float(sum(self.typeDenpendency[eventType].values()))
            for subEventType in CORE_EVENT_TYPES:
                if typeCount > 0:
                    self.typeDenpendency[eventType][subEventType] /= typeCount


    def getTypeDependency(self, leftEventType, rightEventType):
        '''
        Return the type distributions based on the given event type.
        :param eventType:
        :return:
        '''
        return self.typeDenpendency[leftEventType][rightEventType]


if __name__ == '__main__':
    start = time.time()
    fileName = sys.argv[1]
    typeDependencyAnalysisLib = TypeDependencyAnalysisLib(fileName)

    for leftType in CORE_EVENT_TYPES:
        for rightType in CORE_EVENT_TYPES:

            rightTypeIndex = typeDependencyAnalysisLib.coreEventTypes[rightType]
            generalProbability = typeDependencyAnalysisLib.generalTypeDistribution[rightTypeIndex]
            dependentProbability = typeDependencyAnalysisLib.typeDenpendency[leftType][rightType]

            if dependentProbability > 1.3 * generalProbability and generalProbability > 0.05:
                print("%s --> %s"%(leftType, rightType))
                print("General probability: %f" % generalProbability)
                print("Dependent probability: %f" % dependentProbability)
                print(" ")

    end = time.time()
    print("Analyze time: %f"%(end-start))