import calendar
import datetime

from itertools import takewhile
from networkdays import networkdays

(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY) = range(7)



class Day(datetime.date):

    def __init__(self):
        super().__init__(*args, **kwargs)
        self.off = False



class Month(object):
    '''
    Define Year and Month, based on integers, it will give you

        `month.first_date`:      first date of the month
        `month.last_date`:       last date of the month
        `month.month_number`:    the number of the month (jan=1)
        `month.workdays`:        working days in this month
        `month.workdays_number`: Number of working days
        `month.workdays_hours`:  Total comercial hours in the month - base 8
        `month.name`:            name of the month (no local yet)
        `month.abbr_name`:       name abrreviation

    Attributes:
        month_number (TYPE): the number of the month (jan=1) the intance will represents
        year (TYPE): the number of the year the instance will represents.

    return:
        <object worcal.Month>: an object representing the month
    '''

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

    def _get_workdays_month_days(self, month_number):
        '''
        Args:
            month_number (TYPE): Description

        Returns:
            list: a list of month days filtering per month,
                ... [[datetime.datetime(2022, 1, 3, 0, 0), datetime.datetime(2022, 1, 4, 0, 0), datetime.datetime(2022, 1, 5, 0, 0), datetime.datetime(2022, 1, 6, 0, 0), datetime.datetime(2022, 1, 7, 0, 0), datetime.datetime(2022, 1, 10, 0, 0), datetime.datetime(2022, 1, 11, 0, 0), datetime.datetime(2022, 1, 12, 0, 0), datetime.datetime(2022, 1, 13, 0, 0), datetime.datetime(2022, 1, 14, 0, 0), datetime.datetime(2022, 1, 17, 0, 0), datetime.datetime(2022, 1, 18, 0, 0), datetime.datetime(2022, 1, 19, 0, 0), datetime.datetime(2022, 1, 20, 0, 0), datetime.datetime(2022, 1, 21, 0, 0), datetime.datetime(2022, 1, 24, 0, 0), datetime.datetime(2022, 1, 25, 0, 0), datetime.datetime(2022, 1, 26, 0, 0), datetime.datetime(2022, 1, 27, 0, 0), datetime.datetime(2022, 1, 28, 0, 0), datetime.datetime(2022, 1, 31, 0, 0)]]
                into this
                ... [[3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 17, 18, 19, 20, 21, 24, 25, 26, 27, 28, 31]]

            It wouldn't be necessary if
                see https://github.com/cadu-leite/networkdays/issues/18

            todo: https://github.com/cadu-leite/networkdays/issues/18
        '''
        # I could call networkdays limiting per month start , end, bu if for some reason,
        # self.workdays had changed, the result would not be consistent
        #  ... for the last, a lambda inside a itertool funtion is unreadle enought to stil put inside a list comprehension.

        workdays_filtered = list(takewhile(lambda x: x.month == month_number, self.workdays))
        month_workdays = [i.day for i in workdays_filtered]
        return month_workdays

    def _get_week_workdays(self, weekdays, workdays):
        weekdays_filtered = []
        for day in weekdays:
            if day == 0:
                weekdays_filtered.append('_')
            elif day in workdays:
                weekdays_filtered.append(day)
            else:
                weekdays_filtered.append('-')
        return weekdays_filtered

    def get_calendar(self):
        '''
        '_'  (underscore) other months week day
        '-'' (slash) day off (including saturdays and sandays when aplicable)
        <0<number<32> a number between 1 and 31 (inclusive) means work day .
        '''
        cal = calendar.Calendar()
        cal.setfirstweekday(calendar.SUNDAY)
        workdays_monthday = self._get_workdays_month_days(self.month_number)
        newcal = []

        for week in cal.monthdayscalendar(self.year, self.month_number):
            newcal.append(self._get_week_workdays(week, workdays_monthday))
        return newcal



class WCal():

    def iterweekdays(self, firstweekday):
        """
        Returns:
            itertor, content the orderd weekdays with definied start weekday
        list(w.iterweekdays(0)) ---===>[0, 1, 2, 3, 4, 5, 6]
        list(w.iterweekdays(1)) ---===>[1, 2, 3, 4, 5, 6, 0]
        list(w.iterweekdays(2)) ---===>[2, 3, 4, 5, 6, 0, 1]
        list(w.iterweekdays(3)) ---===>[3, 4, 5, 6, 0, 1, 2]
        list(w.iterweekdays(4)) ---===>[4, 5, 6, 0, 1, 2, 3]
        """
        for i in range(firstweekday, firstweekday + 7):
            yield i % 7

    def __init__(self, year=datetime.datetime.now().year, holidays=[]):

        self.year = year
        self.holidays = holidays

        self.date_start = datetime.datetime(self.year, 1, 1, 0, 0)
        self.date_end = datetime.datetime(self.year, 12, 31, 23, 59)
        wdays = networkdays.Networkdays(
            self.date_start,  # start date
            self.date_end,  # end date
            self.holidays  # list of Holidays\
        )
        self.workdays = wdays.networkdays()

    # def get_workdays(self):

    #     return self.workdays


    # def get_calendar(self):
    #     '''
    #     '_'  (underscore) other months week day
    #     '-'' (slash) day off (including saturdays and sandays when aplicable)
    #     <0<number<32> a number between 1 and 31 (inclusive) means work day .
    #     '''
    #     cal = calendar.Calendar()
    #     cal.setfirstweekday(calendar.SUNDAY)
    #     month_workdays = self._get_workdays_month_days(1)

    #     newcal = []

    #     for week in cal.monthdayscalendar(self.year, 1):
    #         newcal.append(self._get_week_workdays(week, month_workdays))

    #     return newcal

