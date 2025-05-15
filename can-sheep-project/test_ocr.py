import unittest
from ocr import ocr
from ocr import functions


class TestDateStringInterpretter(unittest.TestCase):
    date_string = "2025-04-28"
    def test_data_return_dict(self):
        temp_file_path = "./can-sheep-project/tmp/uploaded_file.png"
        extracted_text = ocr.get_encoded_file(temp_file_path)
        data_dict=functions.translate_text(extracted_text, self.date_string)
        self.assertIsInstance(data_dict, dict)

    def test_convert_to_date(self):
        data_dict = {'Date': '28/04/2025', 'Name': 'Samia Ameen', 'Reason for report': 'Movement of animals off farm', 'Date of animal departure': '25/04/2025', 'Date of animal arrival': '26/04/2025', 'PID of departure site': 'PKR 119', 'PID of arrival site': 'MGH 218', 'Time of departure': '9:00 AM', 'Time of arrival': '10:00 PM', 'License plate number or conveyance identification': 'B103 - BX', 'List of identification number(s) on approved indicator': 'HCX 100792 LX 100782', 'Reporting tag retirements': 'No', 'Animals moved to/from community pasture': 'No', 'Reporting approved indicator replacement': 'No', 'New identification number': 'XP4 102', 'PID of site where approved indicator was replaced': 'LHC', 'Acknowledgement': 'Please sign below acknowledging the above information is correct to the best of your knowledge.'}
        possibe_dates=functions.parse_dates(data_dict)
        self.assertEqual(possibe_dates["Departure"], "2025-04-25 09:00")
        self.assertEqual(possibe_dates["Arrival"], "2025-04-26 22:00")

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

if __name__ == "__main__":
    unittest.main()