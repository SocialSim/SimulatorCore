import SocialSimEvaluationEngine.metrics.metrics.RepoCentricMetrics as RepoCentricMetrics
import SocialSimEvaluationEngine.metrics.metrics.TransferEntropy as TransferEntropy
import SocialSimEvaluationEngine.metrics.metrics.UserCentricMetrics as UserCentricMetrics
import SocialSimEvaluationEngine.metrics.metrics.UserMeasurementsWithPlot as UserMeasurementsWithPlot
import SocialSimEvaluationEngine.metrics.metrics.plots
import pandas as pd
import numpy as np

'''
df = pd.DataFrame.from_items([
            ('1',  [ 1, 1, "PushEvent", 1, 1]),
            ('2',  [ 2, 2, "PullEvent", 2, 1]),
            ('3',  [ 3, 3, "PullEvent", 3, 1]),
            ('4',  [ 4, 4, "PushEvent", 1, 1]),
            ('5',  [ 5, 5, "PushEvent", 3, 1]),
            ('6',  [ 6, 6, "PullEvent", 2, 1]),
            ('7',  [ 7, 7, "PushEvent", 4, 1])],
           orient='index', columns=['id', 'time', 'event', 'user', 'repo'])
'''

class EvaluationEngine(object):

    def __init__(self):
        self.onlineSimulationDataFrame = list()
        self.onlineSimulationCount = 0

        self.offlineSimulationDataFrame = list()
        self.groundTruthDataFrame = list()
        self.groundTruthCount = 0
        self.offlineSimulationCount = 0

    def isOnline(self):
        if self.onlineSimulationCount > 0:
            return True
        else:
            return False

    def push(self, event):
        userId = event.getUserID() 
        objId = event.getObjID() 
        eventType = event.getEventType() 
        timestamp = event.getTimestamp() 

        df = (str(self.onlineSimulationCount), [self.onlineSimulationCount, timestamp, eventType, userId, objId])
        self.onlineSimulationDataFrame.append(df)
        self.onlineSimulationCount += 1

    def simulationPush(self, event):
        timestamp = event[0]
        objId = event[1]
        userId = event[2]
        eventType = event[3]

        df = (str(self.offlineSimulationCount), [self.offlineSimulationCount, timestamp, eventType, userId, objId])
        self.offlineSimulationDataFrame.append(df)
        self.offlineSimulationCount += 1

    def groundTruthPush(self, event):
        timestamp = event[0]
        objId = event[1]
        userId = event[2]
        eventType = event[3]

        df = (str(self.groundTruthCount), [self.groundTruthCount, timestamp, eventType, userId, objId])
        self.groundTruthDataFrame.append(df)
        self.groundTruthCount += 1

    def constructPandaFrame(self, dataFrame):
        df = pd.DataFrame.from_items(dataFrame,
             orient='index', columns=['id', 'time', 'event', 'user', 'repo'])
        return df

    def evaluateQuestion18(self, users = list(), plot = False):
        if self.isOnline():
            simulationDataFrame = self.constructPandaFrame(self.onlineSimulationDataFrame)
        else:
            simulationDataFrame = self.constructPandaFrame(self.offlineSimulationDataFrame)

        if plot:
            result = UserMeasurementsWithPlot.getUserUniqueRepos(simulationDataFrame, users)
        else:
            result = UserCentricMetrics.getUserUniqueRepos(simulationDataFrame, users)
        print "=== Evaluation result for question 18 ==="
        print result

        groundTruthDataFrame = self.constructPandaFrame(self.groundTruthDataFrame)
        if plot:
            result = UserMeasurementsWithPlot.getUserUniqueRepos(groundTruthDataFrame, users)
        else:
            result = UserCentricMetrics.getUserUniqueRepos(groundTruthDataFrame, users)
        print "=== Ground truth result for question 18 ==="
        print result

    def evaluateQuestion20(self, users = list(), plot = False):
        if self.isOnline():
            simulationDataFrame = self.constructPandaFrame(self.onlineSimulationDataFrame)
        else:
            simulationDataFrame = self.constructPandaFrame(self.offlineSimulationDataFrame)

        if plot:
            result = UserMeasurementsWithPlot.getUserActivityTimeline(simulationDataFrame, users)
        else:
            result = UserCentricMetrics.getUserActivityTimeline(simulationDataFrame, users)
        print "=== Evaluation result for question 20 ==="
        print result

        groundTruthDataFrame = self.constructPandaFrame(self.groundTruthDataFrame)
        if plot:
            result = UserMeasurementsWithPlot.getUserActivityTimeline(groundTruthDataFrame, users)
        else:
            result = UserCentricMetrics.getUserActivityTimeline(groundTruthDataFrame, users)
        print "=== Ground truth result for question 18 ==="
        print result

    def evaluateQuestion26a(self, eventType = "GITHUB_PUSH", plot = False):
        if self.isOnline():
            simulationDataFrame = self.constructPandaFrame(self.onlineSimulationDataFrame)
        else:
            simulationDataFrame = self.constructPandaFrame(self.offlineSimulationDataFrame)

        if plot:
            result = UserMeasurementsWithPlot.getUserActivityDistribution(simulationDataFrame, eventType)
        else:
            result = UserCentricMetrics.getUserActivityDistribution(simulationDataFrame, eventType)
        print "=== Evaluation result for question 26a ==="
        print result

        groundTruthDataFrame = self.constructPandaFrame(self.groundTruthDataFrame)
        if plot:
            result = UserMeasurementsWithPlot.getUserActivityDistribution(groundTruthDataFrame, eventType)
        else:
            result = UserCentricMetrics.getUserActivityDistribution(groundTruthDataFrame, eventType)
        print "=== Ground truth result for question 18 ==="
        print result

    def evaluateQuestion26b(self, k = 10, plot = False):
        if self.isOnline():
            simulationDataFrame = self.constructPandaFrame(self.onlineSimulationDataFrame)
        else:
            simulationDataFrame = self.constructPandaFrame(self.offlineSimulationDataFrame)

        if plot:
            result = UserMeasurementsWithPlot.getMostActiveUsers(simulationDataFrame, k)
        else:
            result = UserCentricMetrics.getMostActiveUsers(simulationDataFrame, k)
        print "=== Evaluation result for question 26b ==="
        print result

        groundTruthDataFrame = self.constructPandaFrame(self.groundTruthDataFrame)
        if plot:
            result = UserMeasurementsWithPlot.getMostActiveUsers(groundTruthDataFrame, k)
        else:
            result = UserCentricMetrics.getMostActiveUsers(groundTruthDataFrame, k)
        print "=== Groundtruth result for question 26b ==="
        print result

    def evaluateQuestion27(self, k = 10, plot = False):
        if self.isOnline():
            simulationDataFrame = self.constructPandaFrame(self.onlineSimulationDataFrame)
        else:
            simulationDataFrame = self.constructPandaFrame(self.offlineSimulationDataFrame)

        if plot:
            result = UserMeasurementsWithPlot.getUserPopularity(simulationDataFrame, k)
        else:
            result = UserCentricMetrics.getUserPopularity(simulationDataFrame, k)
        topKUser = result
        print "=== Evaluation result for question 27 ==="
        print result

        groundTruthDataFrame = self.constructPandaFrame(self.groundTruthDataFrame)
        if plot:
            result = UserMeasurementsWithPlot.getUserPopularity(groundTruthDataFrame, k)
        else:
            result = UserCentricMetrics.getUserPopularity(groundTruthDataFrame, k)
        print "=== Groundtruth result for question 27 ==="
        print result

        return topKUser


    def evaluateQuestion28Gini(self, plot = False):
        if self.isOnline():
            simulationDataFrame = self.constructPandaFrame(self.onlineSimulationDataFrame)
        else:
            simulationDataFrame = self.constructPandaFrame(self.offlineSimulationDataFrame)

        if plot:
            result = UserMeasurementsWithPlot.getGiniCoef(simulationDataFrame)
        else:
            result = UserCentricMetrics.getGiniCoef(simulationDataFrame)
        print "=== Evaluation result for question 28 with Gini coefficient ==="
        print result

        groundTruthDataFrame = self.constructPandaFrame(self.groundTruthDataFrame)
        if plot:
            result = UserMeasurementsWithPlot.getGiniCoef(groundTruthDataFrame)
        else:
            result = UserCentricMetrics.getGiniCoef(groundTruthDataFrame)
        print "=== Groundtruth result for question 28 with Gini coefficient ==="
        print result

    def evaluateQuestion28Palma(self, plot = False):
        if self.isOnline():
            simulationDataFrame = self.constructPandaFrame(self.onlineSimulationDataFrame)
        else:
            simulationDataFrame = self.constructPandaFrame(self.offlineSimulationDataFrame)

        if plot:
            result = UserMeasurementsWithPlot.getPalmaCoef(simulationDataFrame)
        else:
            result = UserCentricMetrics.getPalmaCoef(simulationDataFrame)
        print "=== Evaluation result for question 28 with Palma coefficient ==="
        print result

        groundTruthDataFrame = self.constructPandaFrame(self.groundTruthDataFrame)
        if plot:
            result = UserMeasurementsWithPlot.getPalmaCoef(groundTruthDataFrame)
        else:
            result = UserCentricMetrics.getPalmaCoef(groundTruthDataFrame)
        print "=== Groundtruth result for question 28 with Palma coefficient ==="
        print result

    def evaluateQuestion29bc(self, users = list(), nCPU = 1, plot = False):
        if self.isOnline():
            simulationDataFrame = self.constructPandaFrame(self.onlineSimulationDataFrame)
        else:
            simulationDataFrame = self.constructPandaFrame(self.offlineSimulationDataFrame)

        if plot:
            result = UserMeasurementsWithPlot.getAvgTimebwEvents(simulationDataFrame, users, nCPU)
        else:
            result = UserCentricMetrics.getAvgTimebwEvents(simulationDataFrame, users, nCPU)
        print "=== Evaluation result for question 29 b and c ==="
        print result

        groundTruthDataFrame = self.constructPandaFrame(self.groundTruthDataFrame)
        if plot:
            result = UserMeasurementsWithPlot.getAvgTimebwEvents(groundTruthDataFrame, users, nCPU)
        else:
            result = UserCentricMetrics.getAvgTimebwEvents(groundTruthDataFrame, users, nCPU)
        print "=== Groundtruth result for question 29 b and c ==="
        print result

    def evaluateQuestion29(self, unit = 's', plot = False):
        if self.isOnline():
            simulationDataFrame = self.constructPandaFrame(self.onlineSimulationDataFrame)
        else:
            simulationDataFrame = self.constructPandaFrame(self.offlineSimulationDataFrame)

        if plot:
            result = UserMeasurementsWithPlot.getUserDiffusionDelay(simulationDataFrame, unit)
        else:
            result = UserCentricMetrics.getUserDiffusionDelay(simulationDataFrame, unit)
        print "=== Evaluation result for question 29 ==="
        print result

        groundTruthDataFrame = self.constructPandaFrame(self.groundTruthDataFrame)
        if plot:
            result = UserMeasurementsWithPlot.getUserDiffusionDelay(groundTruthDataFrame, unit)
        else:
            result = UserCentricMetrics.getUserDiffusionDelay(groundTruthDataFrame, unit)
        print "=== Groundtruth result for question 29 b and c ==="
        print result

    def evaluateByQuestionName(self, questionName):
        pass

