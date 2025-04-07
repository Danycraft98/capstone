from .got_ocr import get_text
from .functions import *

def main():
    # Sample input
    text = get_text("./Sample Form.png")
    # Extract and display dates
    dates = extract_dates(text)
    print("📅 Extracted Dates:")
    for d in dates:
        print(" -", d)

    ocr_text = "SePf"

    # Suggest name corrections
    suggestions = suggest_names(ocr_text)
    print("\n🧠 Name Suggestions for '{}':".format(ocr_text))
    for name in suggestions:
        print(" -", name)


if __name__ == "__main__":
    main()