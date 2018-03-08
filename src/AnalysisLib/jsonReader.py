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
    with open(DATAPATH + "/compressed_event_2015-01-01.txt", "w") as output:
        for hour in range(24):
            fileName = DATAPATH + "/201501/20150101/an_2015-01-01-" + str(hour) + ".json.gz"
            print(fileName)
            eventList = readJson(fileName)
            for event in eventList:
                if count%100 ==0:
                    output.write(event)
                count += 1


