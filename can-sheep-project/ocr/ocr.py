import base64

def get_text(temp_file_path:str)->str:
    from paddleocr import PaddleOCR
    ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
    result = ocr.ocr(temp_file_path, cls=True)
    rtn =""
    for line in result[0]:
        rtn=rtn+" "+line[1][0]  # The text
    return rtn

def get_encoded_file(temp_file_path:str)->str:
    """
    Given a file path, this function reads the file and returns its content as a string.
    """
    with open(temp_file_path, 'rb') as file:
        return  base64.b64encode(file.read()).decode("utf-8")