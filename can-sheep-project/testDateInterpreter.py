from dateInterpreter import interpret_date
import unittest

class TestDateStringInterpretter(unittest.TestCase):
    
    def testdeparture_date_should_be(self):
        actual=interpret_date("Jan 10, 2015", "Jan 12, 2015")
        self.assertDictEqual(actual,{"arrival_date":"2015-01-10", "departure_date":"2015-01-12"})

    def test_if_date_is_lowercase(self):
        actual=interpret_date("jan 10, 2015", "jan 12, 2015")
        self.assertDictEqual(actual,{"arrival_date":"2015-01-10", "departure_date":"2015-01-12"})


    def test_if_comma_is_missing_should_still_work(self):
        actual=interpret_date("Jan 10 2015", "Jan 12 2015")
        self.assertDictEqual(actual,{"arrival_date":"2015-01-10", "departure_date":"2015-01-12"})

    def test_if_month_is_spelled_out(self):
        actual=interpret_date("January 10 2015", "January 12 2015")
        self.assertDictEqual(actual,{"arrival_date":"2015-01-10", "departure_date":"2015-01-12"})

    def test_if_week_day_is_present(self):
        actual=interpret_date("Jan 24, '25 ","Thur Apr 4 2025")
        self.assertDictEqual(actual,{"arrival_date":"2025-04-01", "departure_date":"2025-04-04"}) 

    def test_if_year_is_first_extract_year(self):
        actual=interpret_date("2025, Jan 24 ","Thur Apr 4 2025")
        self.assertDictEqual(actual,{"arrival_date":"2025-04-01", "departure_date":"2025-04-04"}) 