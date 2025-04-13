from dateInterpreter import interpret_date
import unittest

class TestDateStringInterpretter(unittest.TestCase):
    
    def testdeparture_date_should_be(self):
        actual=interpret_date("Jan 10, 2015", "Jan 12, 2015")
        self.assertDictEqual(actual,{"arrival_date":"01-10-2015", "departure_date":"01-12-2015"})
