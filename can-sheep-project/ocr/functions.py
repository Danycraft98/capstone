import re
import nltk
from rapidfuzz import process
from metaphone import doublemetaphone  # pip install Metaphone


nltk.download('names')
from nltk.corpus import names

# Load and normalize names
name_list = list(set(name.lower() for name in names.words()))


def extract_dates(text):
    """
    Extracts date strings from a given text using regular expressions.
    The function is designed to match a variety of date formats typically 
    found in documents or form fields.

    Args:
        text (str): The input text string to search for dates.

    Returns:
        list: A list of matched date strings found in the format 
              "Date <label>: <date>" where <date> matches known patterns.

    Example:
        text = "Date of Birth: 30th March 2025\nAppointment Date: 2025-03-30"
        extract_dates(text)
        # Output: ['30th March 2025', '2025-03-30']
    """
    date_patterns = [
        r'\b(?:\d{1,2}[/-]){2}\d{2,4}\b',                          # 03/30/2025 or 30-03-2025
        r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',                        # 2025-03-30
        r'\b(?:\d{1,2}(?:[a-z]{2})?\s+)?[A-Za-z]{3,}[ ,\-]*\d{2,4}\b',  # 30th March 2025
        r'\b[A-Za-z]{3,}[ ,\-]*\d{1,2}(?:[a-z]{2})?[ ,\-]*\d{2,4}\b',  # March 30th 2025
    ]

    combined_pattern = '|'.join(date_patterns)
    matches = re.findall("Date[\w\s]+:\s+({})".format(combined_pattern), text, re.IGNORECASE)
    return matches


def suggest_names(ocr_text, top_n=10, max_length_diff=1):
    """
    Suggests the most likely intended names based on a noisy OCR-extracted name string.
    This function improves name recognition from OCR text by combining fuzzy matching
    and phonetic similarity techniques.

    Args:
        ocr_text (str): The possibly misspelled or noisy name extracted from OCR.
        top_n (int, optional): Number of top suggested names to return. Defaults to 10.
        max_length_diff (int, optional): Maximum allowed character length difference
                                         between OCR text and candidates. Defaults to 1.

    Returns:
        list: A list of top N suggested names (with capitalization), ranked by similarity.

    Example:
        suggest_names("jhon")  # Might return ['John', 'Joan', 'Shon', ...]
    """
    ocr_text = ocr_text.lower()
    ocr_len = len(ocr_text)

    # Filter name list by length similarity
    length_filtered_names = [name for name in name_list if abs(len(name) - ocr_len) <= max_length_diff]

    # Fuzzy matching
    fuzzy_matches = process.extract(ocr_text, length_filtered_names, limit=50, score_cutoff=50)

    # Phonetic match
    ocr_sound = doublemetaphone(ocr_text)[0]
    phonetic_matches = [
        name for name in length_filtered_names if doublemetaphone(name)[0] == ocr_sound
    ]

    # Combine and deduplicate
    combined = set([match[0] for match in fuzzy_matches] + phonetic_matches)

    # Rerank
    final_matches = process.extract(ocr_text, list(combined), limit=top_n)
    return [match[0].capitalize() for match in final_matches]