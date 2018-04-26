from common.const import *

def temporalPreference(userIds, userCcs):
    '''
    Assemble list of users that will most likely be active each hour given pre-calculated temporal preference distribution 
    :return: nested list of userIds
    '''

    us_userInfo = []
    cn_userInfo = []
    count = 0
    for userId, activity in userIds.iteritems():
        if (userCcs[userId] == "us"):
            us_userInfo.append({"id": userId, "activity": activity, "country_code": userCcs[userId], "index": count})
        else:
            cn_userInfo.append({"id": userId, "activity": activity, "country_code": userCcs[userId], "index": count})
        count += 1

    us_userInfo = sorted(us_userInfo, key = sortKey, reverse = True)
    cn_userInfo = sorted(cn_userInfo, key = sortKey, reverse = True)

    us_pref, cn_pref = loadTemporalPreference()

    total_us_users = len(us_userInfo)
    total_cn_users = len(cn_userInfo)

    print("total_us_users", total_us_users)
    print("total_cn_users", total_cn_users)

    temporal_preference = []
    for i in range(len(us_pref)):
        us_sublist = getActiveUsers(int(total_us_users * us_pref[i]), us_userInfo, "us")
        cn_sublist = getActiveUsers(int(total_cn_users * cn_pref[i]), cn_userInfo, "cn")
        temporal_preference.append(us_sublist + cn_sublist)

    return temporal_preference

def sortKey(d):
    return d["activity"]

def getActiveUsers(active_frac, users, country_code):
    active_user_list = list()
    count = 0
    while count < active_frac:
        active_user_list.append(users[count]["index"])
        count += 1
    return active_user_list

def loadTemporalPreference():
    us_data = []
    with open(US_USER_TEMPORAL_PREFERENCE) as f:
        us_data = f.readlines()

    cn_data = []
    with open(CN_USER_TEMPORAL_PREFERENCE) as f:
        cn_data = f.readlines()

    us_pref = []
    for i in us_data:
        i = i.rstrip("\r")
        subdata = i.split(" ")
        us_pref.append(float(subdata[1]))

    cn_pref = []
    for i in cn_data:
        i = i.rstrip("\r")
        subdata = i.split(" ")
        cn_pref.append(float(subdata[1]))

    return us_pref, cn_pref