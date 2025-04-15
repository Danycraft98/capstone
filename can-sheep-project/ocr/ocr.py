
def get_text(temp_file_path:str)->str:
    from paddleocr import PaddleOCR
    ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
    result = ocr.ocr(temp_file_path, cls=True)
    rtn =""
    for line in result[0]:
        rtn=rtn+line[1][0]  # The text
    return rtn
