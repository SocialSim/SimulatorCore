import time
import os

class SimulationTime(object):
    _instance = None

    @staticmethod
    def getInstance(year, month, day, hour, minute, second):
        '''
        Static access method. The time is in UTC timezone.
        '''
        if SimulationTime._instance is None:
            SimulationTime(year, month, day, hour, minute, second)
        return SimulationTime._instance

    def __init__(self, year, month, day, hour, minute, second):
        if SimulationTime._instance is not None:
            raise Exception("SimulationTime class is a singleton!")
        else:
            SimulationTime._instance = self

        self.year = year
        self.mon = month
        self.day = day
        self.hour = hour
        self.min = minute
        self.sec = second

        # Set the timezone as UTC
        os.environ['TZ'] = "UTC"
        time.tzset()

    def getIsoTime(self, timeShift=0):
        '''
        Convert the current time structure into a string of ISO format.
        You can show the time with a given shift in second, used in the simulation stage to print the time of event.
        :return: A string in the ISO time format.
        '''
        timeTuple = (self.year, self.mon, self.day, self.hour, self.min, self.sec, 0, 0, -1)
        timeStep = time.mktime(timeTuple)
        timeStep += timeShift
        timeTuple = time.gmtime(timeStep)
        iso_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", timeTuple)
        return(iso_time)

    def getYear(self):
        return self.year

    def getMonth(self):
        return self.mon

    def getDay(self):
        return self.day

    def getHour(self):
        return self.hour

    def getMin(self):
        return self.min

    def getSec(self):
        return self.sec

    @staticmethod
    def getHourFromIso(iso_time):
        '''
        Get the hour from a given ISO string. Used in AnalysisLib.
        :param iso_time:
        :return:
        '''
        timeArray = time.strptime(iso_time, "%Y-%m-%dT%H:%M:%SZ")
        return timeArray.tm_hour

    def updateTime(self, yearShift=None, monthShift=None, dayShift=None,
                   hourShift=None, minuteShift=None, secondShift=None):
        '''
        Update the current time.
        :param year:
        :param month:
        :param day:
        :param hour: how
        :param minute:
        :param second:
        :return:
        '''
        shift = 0

        if yearShift:
            shift += yearShift
        shift *= 12

        if monthShift:
            shift += monthShift
        shift *= 30

        if dayShift:
            shift += dayShift
        shift *= 24

        if hourShift:
            shift += hourShift
        shift *= 60

        if minuteShift:
            shift += minuteShift
        shift *= 60

        if secondShift:
            shift += secondShift

        timeTuple = (self.year, self.mon, self.day, self.hour, self.min, self.sec, 0, 0, -1)
        timeTuple = time.struct_time(timeTuple)
        timeStep = time.mktime(timeTuple)
        timeStep += shift
        timeTuple = time.gmtime(timeStep)

        self.year = timeTuple.tm_year
        self.mon = timeTuple.tm_mon
        self.day = timeTuple.tm_mday
        self.hour = timeTuple.tm_hour
        self.min = timeTuple.tm_min
        self.sec = timeTuple.tm_sec


if __name__ == '__main__':
    simulationTime = SimulationTime.getInstance(year=2016,
                               month=5,
                               day=6,
                               hour=3,
                               minute=5,
                               second=6)
    print simulationTime.getIsoTime()
    simulationTime.updateTime(dayShift= 4, hourShift=13)
    timestr = simulationTime.getIsoTime()
    print SimulationTime.getHourFromIso(timestr)


