import re
import nltk
from rapidfuzz import process
from metaphone import doublemetaphone  # pip install Metaphone
import logging
import re
from dotenv import load_dotenv
import os

import datetime

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

logging.getLogger(__name__).setLevel(logging.INFO)
nltk.download("names")
from nltk.corpus import names


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
# Initialize the OpenAI model (use "gpt-4" or "gpt-3.5-turbo")
llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=openai_api_key)

# Load and normalize names
name_list = list(set(name.lower() for name in names.words()))

def translate_text(text):
    from openai import OpenAI

    client = OpenAI()
    # Initialize the ChatOpenAI model with Vision (GPT-4 Vision Preview)
    # chat = ChatOpenAI(
    #     model="gpt-4o",
    #     temperature=0,
    #     max_tokens=2000,
    # )

#--------------
    response = client.responses.create(
    model="gpt-4o",
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "Please extract the text from the image and return it in a JSON format."},
                {"type": "input_image", "image_url": f"data:image/png;base64,{text}"},
            ],
        }
    ],
)
 ##-------------------
 
 
    # Call the model

    logging.info("Calling the model"+str(response))
    returnString=response.output_text.replace("json", '')
    returnString= returnString.replace("```", "")
    return returnString

def parse_dates(text_from_scan):
    """
    Given a scanned text, this function attempts to extract a dictionary of dates.
    It uses regular expressions to find specific date patterns in the text.
    """
    # Correct OCR errors in the extracted text
    corrected_text = correct_ocr_errors(text_from_scan)

    # Extract dates again from the corrected text
    approximate_dates_dict = get_approximate_dateTime(corrected_text)

    # just use the dates to drive
    corrected_dateTime_dict = dict()
    for key in ["departure:", "arrival:"]:
        # Normalize the date to YYYY-MM-DD format
        try:
            corrected_dateTime_dict[key] = tranform_date_to_YYYYMMDD(approximate_dates_dict[key])
        except Exception as e:
            logging.error(f"Error transforming date for key {key}: {e}")
            approximate_dates_dict[key] = "unknown"

    # Return the corrected dates
    return corrected_dateTime_dict



def get_approximate_dateTime(text_from_scan) -> dict:
    """given scanned text try to extarct a dict of date
    and normalize the date to YYYY-MM-DD format
    """
    dateTimeDictionary = dict()
    dateTimeDictionary["submit:"] = extractString(r"date:(.*?)(?=name.*)", text_from_scan)

    departureDate = extractString(
        r"date of animal departure:(.*?)(?=date of animal.*)", text_from_scan
    )
    arrivalDate = extractString(
        r"date of animal arrival:(.*?)(?=pid of departure site:.*)", text_from_scan
    )


    departureTime= extractString(
        r"Time of departure:(.*?)(?=Time of arrival:.*)", text_from_scan
    )
    arrivalTime= extractString(
        r"Time of arrival:(.*?)(?=License plate number.*)", text_from_scan
    )

    dateTimeDictionary["departure:"] = f"{departureDate}  {departureTime}"
    dateTimeDictionary["arrival:"] = f"{arrivalDate}  {arrivalTime}"
    return dateTimeDictionary


def extractString(pattern, text) -> str:
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
    raise ValueError(
        f"unexpected number of parts: {len(myparts)} for pattern {pattern} in text {text}"
    )


def correct_ocr_errors(text) -> str:

    # Define a prompt template for correcting OCR errors
    prompt = PromptTemplate(
        input_variables=["ocr_text"],
        template="The following text was extracted using OCR and may contain errors:\n\n{ocr_text}\n\n"
        "Please correct any errors and return the corrected text.",
    )

    # Create an LLM chain
    ocr_correction_chain = LLMChain(llm=llm, prompt=prompt)

    # Example OCR text with errors
    ocr_text = text

    # Run the chain to correct the OCR text
    corrected_text = ocr_correction_chain.run(ocr_text)
    return corrected_text


def tranform_date_to_YYYYMMDD(date_string):
    """
    Given the date string and the varous formats, defer this work to the LLM
    """
    date_string = date_string.replace("'", "20")
    # Define a prompt template for correcting OCR errors
    prompt = PromptTemplate(
        input_variables=["date_string"],
        template="""Assume the the following date is correct please transform it to "%Y-%m-%d %H:%M format. If the date is 
         ambigious then assume the year field is the field that matches the last for digits of the current year, if there is an appostroy 
        then assume the year follows the appostrophy. If the date is not parsable then return 
        the word "unknown". 


        the date to transform is :\n\n{date_string}\n\n""",
    )

    # Create an LLM chain
    ocr_correction_chain = LLMChain(llm=llm, prompt=prompt)

    # Run the chain to correct the OCR text
    formatted_date = ocr_correction_chain.run(date_string)
    extractedDate = re.split(r"(\d{4}-\d{2}-\d{2} \d{1,2}:\d{1,2})", formatted_date)
    return extractedDate[1] if len(extractedDate) > 1 else "unknown"


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
    length_filtered_names = [
        name for name in name_list if abs(len(name) - ocr_len) <= max_length_diff
    ]

    # Fuzzy matching
    fuzzy_matches = process.extract(
        ocr_text, length_filtered_names, limit=50, score_cutoff=50
    )

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
