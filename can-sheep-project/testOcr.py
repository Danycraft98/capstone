import unittest
from ocr import ocr
from ocr import functions
class TestDateStringInterpretter(unittest.TestCase):
    # def testget_text(self):
    #     temp_file_path = "./can-sheep-project/tmp/uploaded_file.png"
    #     actual = ocr.get_text(temp_file_path)
    #     print(actual)
    #     self.assertIsNotNone(actual )
    
    # def test_if_we_cant_find_a_date(self):
    #     with self.assertRaises(ValueError) as context:
    #         functions.get_approximate_dateTime("no date here matching date of animal departure:(.*?)(?=date of animal.*)") 
    #     self.assertEqual(str(context.exception), "no date here matching date:(.*?)(?=name.*)")

    # def test_if_we_can_find_departure_date(self):
    #     someText=functions.get_approximate_dateTime("""Date: 1-11-23 Name Sepf Houle Reason for report (please circle) Movement of animals off farm Retirement of tag (carcass disposal) Movement of incoming animals Approved indicator replacement M Transportahion of animals Date of animal departure:1S-11-Z3 Date of animal arrival:ICo-ll-Z3 PID of departure site:""")

    #     self.assertEqual(someText["arrival:"], "ICo-ll-Z3")
    #     self.assertEqual(someText["departure:"], "1S-11-Z3")
    #     self.assertEqual(someText["date:"], "1-11-23")
        

    # def test_given_text_extract_approxmate_dates(self):
    #     temp_file_path = "./can-sheep-project/tmp/uploaded_file.png"
    #     extracted_text = ocr.get_text(temp_file_path)
    #     extract_dates=functions.get_approximate_dateTime(extracted_text)
    #     self.assertEqual(extract_dates["arrival:"], "ICo-ll-Z3")
    #     self.assertEqual(extract_dates["departure:"], "1S-11-Z3")
    #     self.assertEqual(extract_dates["date:"], "1-11-23")

    # def test_correct_ocr_errors(self):
    #     temp_file_path = "./can-sheep-project/tmp/uploaded_file.png"
    #     extracted_text = ocr.get_text(temp_file_path)
    #     corrected_text = functions.correct_ocr_errors(extracted_text)
    #     extract_dates=functions.get_approximate_dateTime(corrected_text)
    #     self.assertEqual(extract_dates["Date of animal arrival:"], "16-11-23")
    #     self.assertEqual(extract_dates["Date of animal departure:"], "15-11-23")
    #     self.assertEqual(extract_dates["date:"], "1-11-23")

    # def test_extract_times(self):
    #     temp_file_path = "./can-sheep-project/tmp/uploaded_file.png"
    #     extracted_text = ocr.get_text(temp_file_path)
    #     extracted_text=functions.correct_ocr_errors(extracted_text)
    #     extract_dates=functions.get_approximate_times(dict(),extracted_text)
    #     self.assertEqual(extract_dates["Time of animal departure:"], "23:45")
    #     self.assertEqual(extract_dates["Time of animal arrival:"], "12:45")

    # def test_tranform_date_to_YYYYMMDD_missing_comma(self):
    #     result = functions.tranform_date_to_YYYYMMDD("JUL 23rd 23 14:45 pm")
    #     self.assertEqual(result, "2023-07-23 14:45")


    # def test_tranform_date_to_YYYYMMDD_comma(self):
    #     result = functions.tranform_date_to_YYYYMMDD("JUL 23, 23 12:45 am")
    #     self.assertEqual(result, "2023-07-23 00:45")

    # def test_tranform_date_to_YYYYMMDD_appostrofy(self):
    #     result = functions.tranform_date_to_YYYYMMDD("'23 JUL 21 12:45 pm")
    #     self.assertEqual(result, "2023-07-21 12:45")

    # def test_tranform_date_to_YYYYMMDD_appostrofy(self):
    #     result = functions.tranform_date_to_YYYYMMDD("'23 JUL 21 5:5")
    #     self.assertEqual(result, "2023-07-21 05:05")

    # def test_tranform_date_to_YYYYMMDD_plausible_date_bad_order(self):
    #     result = functions.tranform_date_to_YYYYMMDD("07-21-2023 1:5 pm")
    #     self.assertEqual(result, "2023-07-21 13:05")

    def test_parse_dates_should_return_dict(self):
        temp_file_path = "./can-sheep-project/tmp/uploaded_file.png"
        extracted_text = ocr.get_encoded_file(temp_file_path)
        extract_dates=functions.translate_text(extracted_text)
        self.assertIsInstance(extract_dates, dict)
