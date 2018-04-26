import os
SOCIALSIMPATH = "/Users/Flamino/Virtualenvs/simulator_core/SimulatorCore"
DATAPATH = SOCIALSIMPATH + "/data/"

# constant for DependencyLogger
DEPENDENCY_USER = 0
DEPENDENCY_EVENT = 1
DEPENDENCY_TIMESTAMP = 2

# file for AnalysisLib
STAT_PATH = SOCIALSIMPATH + "/statistics"
USER_ID_FILE = STAT_PATH + "/user_id.json"
USER_CC_FILE = STAT_PATH + "/user_cc.json"
OBJ_ID_FILE = STAT_PATH + "/obj_id.json"
USER_ACTION_RATE_FILE = STAT_PATH + "/user_action_rate.json"
OBJECT_PREFERENCE_FILE = STAT_PATH + "/object_preference.json"
USER_DEPENDENCY_FILE = STAT_PATH + "/user_dependency.json"

# file paths for user temporal preference
US_USER_TEMPORAL_PREFERENCE = STAT_PATH + "/us_action_distribtuion.txt"
CN_USER_TEMPORAL_PREFERENCE = STAT_PATH + "/cn_action_distribtuion.txt"

# output path
LOG_OUTPUT = SOCIALSIMPATH + "/output/"