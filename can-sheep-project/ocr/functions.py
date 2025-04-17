import re
import nltk
from rapidfuzz import process
from metaphone import doublemetaphone  # pip install Metaphone
import logging
import re
from dotenv import load_dotenv
import os

logging.getLogger(__name__).setLevel(logging.INFO)
nltk.download('names')
from nltk.corpus import names


load_dotenv()
# Load and normalize names
name_list = list(set(name.lower() for name in names.words()))

def parse_dates(text_from_scan):
    """
    Given a scanned text, this function attempts to extract a dictionary of dates.
    It uses regular expressions to find specific date patterns in the text.
    """
    
    # Correct OCR errors in the extracted text
    corrected_text = correct_ocr_errors(text_from_scan)
    
    # Extract dates again from the corrected text
    corrected_date_dict = get_approximate_dates(corrected_text)
    
    # Return the corrected dates
    return corrected_date_dict



def get_approximate_dates(text_from_scan) -> dict:
    """ given scanned text try to extarct a dict of date"""
    dateDictionary = dict()
    pattern = r'date:(.*?)(?=name.*)'
    dateDictionary["date:"] = extractDate(pattern ,text_from_scan)
    dateDictionary["Date of animal departure:"] = extractDate(r'date of animal departure:(.*?)(?=date of animal.*)'
                                                              ,text_from_scan)
    dateDictionary["Date of animal arrival:"] = extractDate(r'date of animal arrival:(.*?)(?=pid of departure site:.*)'
                                                              ,text_from_scan)
    return dateDictionary

def extractDate(pattern, text)->str:
    """
    Extracts a date based on the given pattern from the provided text.
    Handles multiline text by using the re.DOTALL flag.
    """
    # Match the pattern across multiple lines
    if re.search(pattern, text, re.IGNORECASE | re.DOTALL) is None:
        raise ValueError(f"no date here matching {pattern}")

    # Split the text based on the pattern
    myparts = re.split(pattern, text, flags=re.IGNORECASE | re.DOTALL)
    if len(myparts) == 3:
        # If we have more than one part, return the first part after the pattern
        return myparts[1].strip()
    # for i in range(len(myparts)):
    #     if "date:" in myparts[i].lower():
    #         # If we found the date part, return it
    #         return myparts[i + 1].strip()
    raise ValueError(f"unexpected number of parts: {len(myparts)} for pattern {pattern} in text {text}")

def correct_ocr_errors(text):
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain

    openai_api_key = os.getenv("OPENAI_API_KEY")
    # Initialize the OpenAI model (use "gpt-4" or "gpt-3.5-turbo")
    llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=openai_api_key)

    # Define a prompt template for correcting OCR errors
    prompt = PromptTemplate(
        input_variables=["ocr_text"],
        template="The following text was extracted using OCR and may contain errors:\n\n{ocr_text}\n\n"
                "Please correct any errors and return the corrected text."
    )

    # Create an LLM chain
    ocr_correction_chain = LLMChain(llm=llm, prompt=prompt)

    # Example OCR text with errors
    ocr_text = text

    # Run the chain to correct the OCR text
    corrected_text = ocr_correction_chain.run(ocr_text)
    return corrected_text


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