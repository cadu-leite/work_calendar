import unittest

from workcal.workcal import WCal
from workcal.workcal import Month

import datetime
from unittest import mock

class TestClassMonth(unittest.TestCase):

    def test_import_Month(self):
        '''
        We have a class
        '''
        m = Month(2021, 2)
        self.assertIsInstance(m, Month)

    def test_month_number_setter(self):
        '''
        month_number setter
        '''
        m = Month(2021, 2)
        self.assertEqual(m.month_number, 2)

    def test_month_number_setter_called(self):
        '''
        month setter called
        '''
        with mock.patch('workcal.workcal.Month.month_number', new_callable=mock.PropertyMock) as month_number_patched:
            month_number_patched.reset_mock()  # ... so  <<<< todo: check TRICKY! ?!?!
            Month(2021, 2)
            month_number_patched.assert_called_once_with(2)

    def test_month_number_sets_first_date(self):
        '''
        month setter sets `first_date`
        '''
        m = Month(2021, 2)
        self.assertEqual(m.first_date, datetime.datetime(2021, 2, 1, 0, 0))

    def test_month_number_sets_last_date(self):
        '''
        month setter sets `last_date`
        '''
        m = Month(2021, 2)
        self.assertEqual(m.last_date, datetime.datetime(2021, 2, 28, 23, 59))

    def test__get_month_limits_dates_tuple(self):
        '''
        first and last dates of month
        '''
        m = Month(2021, 2)
        dates = m._get_month_limits_dates_(2)

        first = datetime.datetime(m.year, 2, 1, 0, 0)
        last = datetime.datetime(m.year, 2, 28, 23, 59)

        self.assertEqual(dates, tuple((first, last)))

    def test_month_work_days(self):
        '''
        workdays attributes set
        '''
        m = Month(2021, 2)
        # self.assertEqual(m.workdays, )  # not test 3rd part lib
        self.assertEqual(m.workdays_number, 20, 'Workdays number calc')
        self.assertEqual(m.workdays_hours, 160, 'Woarkdays hours calc')


class TestClassWorkCalendar(unittest.TestCase):


    def test_import(self):
        '''
        We have a class
        '''
        w = WCal()
        self.assertIsInstance(w, WCal)

    def test_year_got_default(self):
        '''
        Current Year if none is set.
        '''
        w = WCal()
        self.assertEqual(w.year, datetime.datetime.now().year)

    def test_year_set_non_default(self):
        '''
        Current Year was set, its not default.
        '''
        w = WCal(2022)
        self.assertEqual(w.year, 2022)



    # def teste_get_number_workdays(self):
    #     '''
    #     Number of workdays of given date range
    #     '''
    #     HOLIDAYS = {datetime.datetime(2020, 12, 25), }
    #     days = networkdays.Networkdays(
    #         datetime.datetime(2020, 12, 15, 0, 0),  # start date
    #         datetime.datetime(2020, 12, 31, 23, 59),  # end date
    #         HOLIDAYS  # list of Holidays
    #     )
    #     ndays = (days.networkdays())

    #     cal = calendar.Calendar()
    #     cal.setfirstweekday(calendar.SUNDAY)

    #     print(f'==>>[] cal.monthdatesscalendar(2021,1) => [{cal.monthdayscalendar(2021,1)}]')

    #     print(f'==>>[] cal.monthdayscalendar(2021,1) => [{cal.monthdays2calendar(2021,1)}]')

    #     print(f'==>>[] cal.monthdays2calendar(2021,1) => [{cal.monthdays2calendar(2021,1)}]')

    #     print(f'==>>[] calendar.monthrange(2021,2) => [{calendar.monthrange(2021,2)}]')

