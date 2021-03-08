import datetime
from networkdays import networkdays
import calendar


class Month(object):
    """docstring for Month"""
    def __init__(self, year, month_number):
        self.year = year
        self.month_number = month_number

    @property
    def first_date(self):
        return self._first_date

    @property
    def last_date(self):
        return self._last_date

    @property
    def month_number(self):
        # to read property self.month_number
        return self._month_number

    @month_number.setter
    def month_number(self, value):
        self._first_date, self._last_date = self._get_month_limits_dates_(value)
        self._workdays = networkdays.Networkdays(self._first_date, self._last_date).networkdays()
        self._month_number = value

    @property
    def workdays(self):
        return self._workdays

    @property
    def workdays_number(self):
        return len(self._workdays)

    @property
    def workdays_hours(self, workhoursperday=8):
        return len(self._workdays) * workhoursperday

    @property
    def name(self):
        return calendar.month_name[self.start.month + 1]

    @property
    def abbr_name(self):
        return calendar.month_abbr()[self.start.month + 1]

    def _get_month_limits_dates_(self, month_number):
        '''
        Args:
            month (integer): Description

        Returns:
            Tuple: returns a tuple, with first and last datetime of a month
        '''
        first_month_date = datetime.datetime(self.year, month_number, 1, 0, 0)

        last_month_day = calendar.monthrange(self.year, month_number)[1]
        last_month_date = datetime.datetime(self.year, month_number, last_month_day, 23, 59)
        return tuple((first_month_date, last_month_date))


class WCal():
    def __init__(self, year=datetime.datetime.now().year, holidays=[]):
        self.year = year
        self.holidays = holidays

        self.date_start = datetime.datetime(self.year, 1, 1, 0, 0)
        self.date_end = datetime.datetime(self.year, 12, 31, 23, 59)
        self.workdays = networkdays.Networkdays(
            self.date_start,  # start date
            self.date_end,  # end date
            self.holidays  # list of Holidays\
        )


