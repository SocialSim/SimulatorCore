import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import json
import time
import sys
import common.analysisArgParser as argParser
from common.const import *
from sklearn import linear_model
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import PolynomialFeatures
from multiprocessing import Pool
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.stattools import arma_order_select_ic

def extractData(fileName):
    '''
    Extract user record from the given file.
    Note: This function can not be member function of class for purpose of multi-processing use.
    :param fileName:
    :return:
    '''
    print fileName
    userRecords = []
    with open(fileName, 'rb') as file:
        for line in file:
            record = json.loads(line)
            userId = record["ght_id_h"]
            creationTime = record["created_at"]
            creationDoW = record["extension"]["created_dow"]
            userRecords.append((userId, creationTime, creationDoW))

    return userRecords

class UserCreationAnalysisLib:
    _instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if UserCreationAnalysisLib._instance is None:
            UserCreationAnalysisLib()
        return UserCreationAnalysisLib._instance

    def __init__(self):
        if UserCreationAnalysisLib._instance is not None:
            raise Exception("UserCreationAnalysisLib class is a singleton!")
        else:
            UserCreationAnalysisLib._instance = self

        # Prepare the data
        print("Preparing data...")
        self.dataPreparation()

        # Daily distribution analysis
        print("Analyze daily distribution...")
        self.dailyDistributionAnalysis()

        # Weekly regression
        print("Weekly regression...")
        self.weeklyRegression()


    def dataPreparation(self):
        fileList = []
        for i in range(0, 8):
            fileName = DATAPATH + "User_Profile/an_users_" + str(i) + ".json"
            fileList.append(fileName)

        pool = Pool(len(fileList))
        userRecords = np.vstack(np.array(pool.map(extractData, fileList)))
        pool.close()
        pool.join()

        self.df = pd.DataFrame(data=userRecords, columns=['UserId', 'CreationTime', 'CreationDoW'])
        self.df["CreationTime"] = pd.to_datetime(self.df["CreationTime"])


    def dailyDistributionAnalysis(self):
        '''
        Analyze the creation of new users within one week.
        :return:
        '''
        # Weedkday distribution
        weekDayCount = self.df.loc[:, ['CreationDoW']]
        weekDayCount['Count'] = 1
        weekDayCount = weekDayCount.groupby('CreationDoW').sum().reset_index()
        index = weekDayCount.values[:, 0]
        value = weekDayCount.values[:, 1] / float(sum(weekDayCount.values[:, 1]))
        self.weekDayDistribution = dict(zip(index, value))
        # print self.weekDayDistribution


    def weeklyRegression(self):
        '''
        Do regression on the creation of users based on weekly number.
        :return:
        '''
        # self.weekIndex = pd.date_range(start='2015-01-01', end='2017-08-31', freq='W')
        weekCount = self.df.loc[:, ['CreationTime']]
        weekCount['Count'] = np.float(1)
        weekCount = weekCount.groupby(pd.Grouper(freq='W', key='CreationTime')).sum()

        # Drop two weeks(Sunday) with unusually many creations.
        # weekCount = weekCount.drop(index=[pd.Timestamp('2015-08-23'), pd.Timestamp('2016-04-24')])

        # Linear Regression
        x = np.array(weekCount.index.view('int64')) // pd.Timedelta(1, unit='s')
        x = x.reshape(-1, 1) / (3600 * 24 * 7)
        y = np.array(weekCount.values).flatten()
        self.regressor = linear_model.LinearRegression(n_jobs=-1)
        self.regressor.fit(x, y)
        y_predict = self.regressor.predict(x)

        # Polynomial regression
        poly = PolynomialFeatures(degree=2)
        x_ = poly.fit_transform(x)
        poly_regressor = linear_model.LinearRegression(n_jobs=-1)
        poly_regressor.fit(x_, y)
        y_poly_predict = poly_regressor.predict(x_)

        # SVM regression
        # svr = SVR()
        # svr.fit(x, y)
        # y_svr_predict = svr.predict(x)

        # Multi layer perceptron
        # mlp = MLPRegressor()
        # mlp.fit(x, y)
        # y_mlp_predict = mlp.predict(x)

        # Auto regressive model
        ar = AR(weekCount, freq='W').fit(maxlag=50, ic='aic')
        y_ar_predict = ar.predict()
        ar_order = ar.k_ar
        print("AR model order: %d" % ar_order)

        # ARMA model
        arma_order = arma_order_select_ic(weekCount, ic='aic')['aic_min_order']
        print("ARMA model order: (%d, %d)" % (arma_order[0], arma_order[1]))
        arma = ARMA(weekCount, arma_order).fit(disp=-1)
        y_arma_predict = arma.predict()

        print("Week, Groundtruth, Linear Model, AR Model")
        for i in range(len(x)-52, len(x)):
            print(str(x[i][0]) + " " + str(int(y[i])) + " " + str(int(y_predict[i])) + " " + str(int(y_ar_predict[i-ar_order])))

        # print(len(x), len(y_predict), len(y_ar_predict), len(y_arma_predict))

        # print('Coefficients of linear model: %f' % self.regressor.coef_)
        print("Mean absolute error of linear model: %.2f" % mean_absolute_error(y, y_predict))
        print("Mean absolute error of PolyNomial model: %.2f" % mean_absolute_error(y, y_poly_predict))
        # print("Mean absolute error of SVM model: %.2f" % mean_absolute_error(y, y_svr_predict))
        # print("Mean absolute error of MLP model: %.2f" % mean_absolute_error(y, y_mlp_predict))
        print("Mean absolute error of AR model: %.2f" % mean_absolute_error(y[ar_order:], y_ar_predict))
        print("Mean absolute error of ARMA model: %.2f" % mean_absolute_error(y, y_arma_predict))


    def getNewUserNumber(self, timeStep, dow):
        '''
        Given the day, return the predicted new user numbers for this day.
        :param timeStep:
        :param dayOfWeek:
        :return:
        '''
        weekTotal = self.regressor.predict([timeStep])[0]
        dayProportion = self.weekDayDistribution[dow]
        return int(weekTotal * dayProportion)


if __name__ == '__main__':
    start = time.time()
    analysisLib = UserCreationAnalysisLib()
    end = time.time()
    print("Analyzing time: %f s" % (end-start))
