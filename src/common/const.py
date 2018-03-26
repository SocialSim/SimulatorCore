import os
import numpy as np
SOCIALSIMPATH = os.environ['SOCIALSIMPATH']
DATAPATH = SOCIALSIMPATH + "/data/"

# constant for DependencyLogger
DEPENDENCY_USER = 0
DEPENDENCY_EVENT = 1
DEPENDENCY_TIMESTAMP = 2

# constant for user clustering
INACTIVE_THRESHOLD = 0.2
ACTIVE_THRESHOLD = 5
ANALYSIS_LENGTH = 31

# file for AnalysisLib
STAT_PATH = SOCIALSIMPATH + "/statistics"
USER_ID_FILE = STAT_PATH + "/user_id.json"
CLUSTER_ID_FILE = STAT_PATH + "/cluster_id.json"
OBJ_ID_FILE = STAT_PATH + "/obj_id.json"
USER_ACTION_RATE_FILE = STAT_PATH + "/user_action_rate.json"
CLUSTER_ACTION_RATE_FILE = STAT_PATH + "/cluster_action_rate.json"
USER_OBJECT_PREFERENCE_FILE = STAT_PATH + "/user_object_preference.json"
USER_TYPE_DISTRIBUTION_FILE = STAT_PATH + "/user_type_distribution.json"
CLUSTER_TYPE_DISTRIBUTION_FILE = STAT_PATH + "/cluster_type_distribution.json"
CLUSTER_MEMBER_FILE = STAT_PATH + "/cluster_member.json"
USER_DEPENDENCY_FILE = STAT_PATH + "/user_dependency.json"

# constant for event types
EVENT_TYPEs = ["CommitCommentEvent", "CreateEvent", "DeleteEvent", "ForkEvent", "IssueCommentEvent",
              "IssuesEvent", "PullRequestEvent", "PushEvent", "WatchEvent", "PublicEvent",
              "MemberEvent", "GollumEvent", "ReleaseEvent", "PullRequestReviewCommentEvent"]

CORE_EVENT_TYPES = ["CreateEvent", "DeleteEvent", "ForkEvent",
                       "IssuesEvent", "PullRequestEvent", "PushEvent", "WatchEvent"]

TYPE_INDEX = np.arange(14)
