import os
import numpy as np
SOCIALSIMPATH = os.environ['SOCIALSIMPATH']
DATAPATH = SOCIALSIMPATH + "/data/"

# constant for DependencyLogger
DEPENDENCY_USER = 0
DEPENDENCY_EVENT = 1
DEPENDENCY_TIMESTAMP = 2

# file for AnalysisLib
STAT_PATH = SOCIALSIMPATH + "/statistics"
USER_ID_FILE = STAT_PATH + "/user_id.json"
OBJ_ID_FILE = STAT_PATH + "/obj_id.json"
USER_ACTION_RATE_FILE = STAT_PATH + "/user_action_rate.json"
OBJECT_PREFERENCE_FILE = STAT_PATH + "/object_preference.json"
TYPE_DISTRIBUTION_FILE = STAT_PATH + "/type_distribution.json"
USER_DEPENDENCY_FILE = STAT_PATH + "/user_dependency.json"

# constant for event types
EVENT_TYPEs = ["CommitCommentEvent", "CreateEvent", "DeleteEvent", "ForkEvent", "IssueCommentEvent",
              "IssuesEvent", "PullRequestEvent", "PushEvent", "WatchEvent", "PublicEvent",
              "MemberEvent", "GollumEvent", "ReleaseEvent", "PullRequestReviewCommentEvent"]

TYPE_INDEX = np.arange(14)
