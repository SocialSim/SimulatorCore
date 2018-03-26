from common.const import *
import json
import gzip
import time


def convertTime(iso_time):
    timeArray = time.strptime(iso_time, "%Y-%m-%dT%H:%M:%SZ")
    timeStamp = time.mktime(timeArray)
    return int(timeStamp)

def extractEvent(record):
    userId = record["actor"]["id_h"]
    objectId = record["repo"]["id_h"]
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
    with open(DATAPATH + "ISO-time-event_2015.txt", "w") as output:
        for month in range(1, 13):
            for day in range(1, monthlyDay[month-1]+1):
                for hour in range(24):
                    fileName = DATAPATH + "Events/Anon/2015" + str(month).zfill(2) + "/2015" + \
                               str(month).zfill(2) + str(day).zfill(2)\
                               + "/an_2015-"+str(month).zfill(2)+"-" + \
                               str(day).zfill(2) + "-" + str(hour) + ".json.gz"
                    print(fileName)
                    eventList = readJson(fileName)
                    for event in eventList:
                        output.write(event)


