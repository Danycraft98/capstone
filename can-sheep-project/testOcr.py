import unittest
from ocr import ocr
class TestDateStringInterpretter(unittest.TestCase):
    def testget_text(self):
        temp_file_path = "./can-sheep-project/temp_file_dir/uploaded_file.png"
        actual = ocr.get_text(temp_file_path)
        print(actual)