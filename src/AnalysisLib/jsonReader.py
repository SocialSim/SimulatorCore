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
    eventTime = convertTime(record["created_at"])
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

    count = 0
    with open(DATAPATH + "event_2015-02.txt", "w") as output:
        for day in range(20150201,20150229):
            for hour in range(24):
                fileName = DATAPATH + "Events/Anon/201502/" + str(day) + "/an_2015-02-" + \
                           str(day%100).zfill(2) + "-" + str(hour) + ".json.gz"
                print(fileName)
                eventList = readJson(fileName)
                for event in eventList:
                    if count%1 == 0:
                        output.write(event)
                    count += 1


