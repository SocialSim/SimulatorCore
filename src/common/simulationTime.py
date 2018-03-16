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

    @staticmethod
    def getIsoTime(timeShift=0):
        '''
        Convert the current time structure into a string of ISO format.
        You can show the time with a given shift in second, used in the simulation stage to print the time of event.
        :return: A string in the ISO time format.
        '''
        timeTuple = (SimulationTime._instance.year,
                     SimulationTime._instance.mon,
                     SimulationTime._instance.day,
                     SimulationTime._instance.hour,
                     SimulationTime._instance.min,
                     SimulationTime._instance.sec, 0, 0, -1)
        timeStep = time.mktime(timeTuple)
        timeStep += timeShift
        timeTuple = time.gmtime(timeStep)
        iso_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", timeTuple)
        return(iso_time)

    @staticmethod
    def getYear():
        return SimulationTime._instance.year

    @staticmethod
    def getMonth():
        return SimulationTime._instance.mon

    @staticmethod
    def getDay():
        return SimulationTime._instance.day

    @staticmethod
    def getHour():
        return SimulationTime._instance.hour

    @staticmethod
    def getMin():
        return SimulationTime._instance.min

    @staticmethod
    def getSec():
        return SimulationTime._instance.sec

    @staticmethod
    def getHourFromIso(iso_time):
        '''
        Get the hour from a given ISO string. Used in AnalysisLib.
        :param iso_time:
        :return:
        '''
        timeArray = time.strptime(iso_time, "%Y-%m-%dT%H:%M:%SZ")
        return timeArray.tm_hour

    @staticmethod
    def updateTime(yearShift=None, monthShift=None, dayShift=None,
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

        timeTuple = (SimulationTime._instance.year,
                     SimulationTime._instance.mon,
                     SimulationTime._instance.day,
                     SimulationTime._instance.hour,
                     SimulationTime._instance.min,
                     SimulationTime._instance.sec, 0, 0, -1)
        timeTuple = time.struct_time(timeTuple)
        timeStep = time.mktime(timeTuple)
        timeStep += shift
        timeTuple = time.gmtime(timeStep)

        SimulationTime._instance.year = timeTuple.tm_year
        SimulationTime._instance.mon = timeTuple.tm_mon
        SimulationTime._instance.day = timeTuple.tm_mday
        SimulationTime._instance.hour = timeTuple.tm_hour
        SimulationTime._instance.min = timeTuple.tm_min
        SimulationTime._instance.sec = timeTuple.tm_sec


if __name__ == '__main__':
    SimulationTime.getInstance(year=2016,
                               month=5,
                               day=6,
                               hour=3,
                               minute=5,
                               second=6)
    print SimulationTime.getIsoTime()
    SimulationTime.updateTime(dayShift= 4, hourShift=13)
    timestr = SimulationTime.getIsoTime()
    print SimulationTime.getHourFromIso(timestr)


