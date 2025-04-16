import unittest
from ocr import ocr
from ocr import functions
class TestDateStringInterpretter(unittest.TestCase):
    def testget_text(self):
        temp_file_path = "./can-sheep-project/temp_file_dir/uploaded_file.png"
        actual = ocr.get_text(temp_file_path)
        print(actual)
        self.assertIsNotNone(actual )
    
    def test_if_we_cant_find_a_date(self):
        with self.assertRaises(ValueError) as context:
            functions.get_approximate_dates("some baloney string date:Name") 
        self.assertEqual(str(context.exception), "no date here matching (\s*date:)(.*)(name.*)")

    def test_if_we_can_find_departure_date(self):
        someText=functions.get_approximate_dates("""Date: 1-11-23 Name Sepf Houle Reason for report (please circle) Movement of animals off farm Retirement of tag (carcass disposal) Movement of incoming animals Approved indicator replacement M Transportahion of animals Date of animal departure:1S-11-Z3 Date of animal arrival:ICo-ll-Z3 PID of departure site:""")

        self.assertEqual(someText["Date of animal arrival:"], "ICo-ll-Z3")
        self.assertEqual(someText["Date of animal departure:"], "1S-11-Z3")
        self.assertEqual(someText["date:"], "1-11-23")
        # self.assertDictEqual(someText, {"date:":"1-11-23",  
        #                                 "Date of animal departure:":"1S-11-Z3",
        #                                 "Date of animal arrival:":"ICo-ll-Z3"
        #                                 } ) 
        

    def test_given_text_extract_approxmate_dates(self):
        temp_file_path = "./can-sheep-project/temp_file_dir/uploaded_file.png"
        extracted_text = ocr.get_text(temp_file_path)
        extract_dates=functions.get_approximate_dates(extracted_text)
        self.assertEqual(extract_dates["Date of animal arrival:"], "ICo-ll-Z3")
        self.assertEqual(extract_dates["Date of animal departure:"], "1S-11-Z3")
        self.assertEqual(extract_dates["date:"], "1-11-23")