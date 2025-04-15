from .got_ocr import get_text
from .functions import *
from .circled import extract_circled_texts

def main():
    image_path = "./Sample Form.png"

    # Sample input
    text = get_text()
    # Extract and display dates
    dates = extract_dates(text)
    print("Extracted Dates:")
    for d in dates:
        print(" -", d)

    ocr_text = "SePf"

    # Suggest name corrections
    suggestions = suggest_names(ocr_text)
    print("\nName Suggestions for '{}':".format(ocr_text))
    for name in suggestions:
        print(" -", name)
        
    results = extract_circled_texts(image_path, debug=True)

    print("Open Circled Texts Found:")
    for idx, text in enumerate(results):
        print(f"{idx+1}: {text}")



if __name__ == "__main__":
    main()