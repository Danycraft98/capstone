import unittest
from ocr import ocr
from ocr import functions

class TestDateStringInterpretter(unittest.TestCase):
    def testget_text(self):
        temp_file_path = "./can-sheep-project/temp_file_dir/travis_bickle.png"
        encodedFile= ocr.get_encoded_file(temp_file_path)
        data_dict=functions.translate_text(encodedFile, "2025-04-28")
        self.assertIsNotNone(data_dict)

    def testsave_to_mongo(self):
        functions.save_to_mongo({"k":"v"})
        self.assertTrue(True)

    # def test_data_return_dict(self):
    #     temp_file_path = "./can-sheep-project/tmp/uploaded_file.png"
    #     extracted_text = ocr.get_encoded_file(temp_file_path)
    #     data_dict=functions.translate_text(extracted_text)
    #     self.assertIsInstance(data_dict, dict)



if __name__ == '__main__':
    unittest.main()