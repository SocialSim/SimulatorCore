from common.const import *
import json
import gzip
import time
import sys


def convertTime(iso_time):
    timeArray = time.strptime(iso_time, "%Y-%m-%dT%H:%M:%SZ")
    timeStamp = time.mktime(timeArray)
    return int(timeStamp)

def extractEvent(record):

    if "id_h" in record["actor"]:
        userId = record["actor"]["id_h"]
    else:
        userId = "None"

    if "id_h" in record["repo"]:
        objectId = record["repo"]["id_h"]
    else:
        objectId = "None"
    # eventTime = convertTime(record["created_at"])
    eventTime = record["created_at"]
    eventType = record["type"]
    return str(eventTime) + " " + str(objectId) + " " + str(userId) + " " + str(eventType) + "\n"

def readJson(filename):
    eventList = []
    with gzip.open(filename, 'rb') as f:
        for line in f:
            event = extractEvent(json.loads(line))
            eventList.append(event)
    return eventList

if __name__ == '__main__':

    monthlyDay = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # for year in range(2015, 2018):
    #     for month in range(1, 13):
    #         if year == 2017 and month > 8:
    #             break
    year = int(sys.argv[1][0: 4])
    month = int(sys.argv[1][4: 6])
    outputFile = DATAPATH + "Monthly_Events/ISO-time-event_" + str(year) + "-" + str(month).zfill(2) + ".txt"
    print(outputFile)
    with open(outputFile, "w") as output:
        for day in range(1, monthlyDay[month - 1] + 1):
            for hour in range(24):
                fileName = DATAPATH + "Events/Anon/"+ str(year) + str(month).zfill(2) + "/" + str(year) + \
                           str(month).zfill(2) + str(day).zfill(2) \
                           + "/an_"+str(year)+"-" + str(month).zfill(2) + "-" + \
                           str(day).zfill(2) + "-" + str(hour) + ".json.gz"
                print(fileName)
                eventList = readJson(fileName)
                for event in eventList:
                    output.write(event)


