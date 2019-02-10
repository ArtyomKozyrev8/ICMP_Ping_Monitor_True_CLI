import enum
import time


class MyTimeMode(enum.Enum):
    '''This class is created to be used in instances of MyTime class
     to determine options of __str__ format for that class'''
    full = "Date: {2}.{1}.{0} Time UTC+3 {3}:{4}:{5}"
    middle = "date{2}_{1}_{0}_timeUTC3_{3}"
    short = "date{2}_{1}_{0}"


class MyTime:
    '''This class is used to display datetime in this program'''

    def __init__(self, mode=MyTimeMode.middle):
        ''' Is used to create class instance'''
        self.timeNow = time.localtime()
        self.mode = mode

    def __str__(self):
        '''Is used to create string representation of the MyTime Class to be used in print, etc'''

        time_now = [self.timeNow.tm_mday, self.timeNow.tm_mon, self.timeNow.tm_year,
                    self.timeNow.tm_hour, self.timeNow.tm_min, self.timeNow.tm_sec]

        time_now_formatted = map(lambda x: str(x).rjust(2, '0'), time_now)

        return self.mode.value.format(*time_now_formatted)  # value is an attribute of enum class

    def compare_dates(self, date_compare):
        '''The class is used to compare instance of MyTime Class'''
        t1 = (self.timeNow.tm_year, self.timeNow.tm_mon,
              self.timeNow.tm_mday, self.timeNow.tm_hour)
        t2 = (date_compare.timeNow.tm_year, date_compare.timeNow.tm_mon,
              date_compare.timeNow.tm_mday, date_compare.timeNow.tm_hour)
        return t1 > t2
#
