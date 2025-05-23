import os
import re
import json
import nltk
import logging
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

logging.getLogger(__name__).setLevel(logging.INFO)
nltk.download("names")
from nltk.corpus import names


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
# Initialize the OpenAI model (use "gpt-4" or "gpt-3.5-turbo")
llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=openai_api_key)

# Load and normalize names
name_list = list(set(name.lower() for name in names.words()))

def translate_text(text, date_string ):
    logging.info("Translating text from image")
    from openai import OpenAI

    client = OpenAI()
    # Initialize the ChatOpenAI model with Vision (GPT-4 Vision Preview)
    # chat = ChatOpenAI(
    #     model="gpt-4o",
    #     temperature=0,
    #     max_tokens=2000,
    # )
    
    promptStr=f"""You are an excellent data entry specialist that is really good at understanding hand written data.
    
    extract the text from the image and return it in a JSON format. Change all the dates to the format YYYY-MM-DD.
    Assume that all the dates are three with in three weeks of {date_string} and animal departure is always before
    animal arrival.
    """
    response = client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": promptStr},
                    {"type": "input_image", "image_url": f"data:image/png;base64,{text}"},
                ],
            }
        ],
    )
 
 
    # Call the model

    logging.info("Calling the model"+str(response))
    returnString = response.output_text.replace("json", '')
    returnString = json.loads(returnString.replace("```", ""))
    return returnString


def parse_dates(data_dict):
    """
    Given a scanned text, this function attempts to extract a dictionary of dates.
    It uses regular expressions to find specific date patterns in the text.
    """
    logging.info("Parsing dates from the data dictionary")
    raw_datetime = {"Departure": [], "Arrival": []}
    for field in sorted(data_dict):
        if not re.search("(?:date|time)[ _]+of", field.lower()):
            continue
        
        key = "Departure" if "departure" in field.lower() else "Arrival"
        raw_datetime[key].append(data_dict[field])

    dates = {}
    for key in raw_datetime:
        datetime_val = " ".join(raw_datetime[key])

        # Normalize the date to YYYY-MM-DD format
        try:
            dates[key] = tranform_date_to_YYYYMMDD(datetime_val)
        except Exception as e:
            logging.error(f"Error transforming date for key {key}: {e}")
            dates[key] = "unknown"
    
    return dates


def tranform_date_to_YYYYMMDD(date_string):
    """
    Given the date string and the varous formats, defer this work to the LLM
    """
    date_string = date_string.replace("'", "20")
    # Define a prompt template for correcting OCR errors
    prompt = PromptTemplate(
        input_variables=["date_string"],
        template="""
                    Assume the the following datetime is correct please transform it to "%Y-%m-%d %H:%M format. If the date is 
                    ambigious then assume the year field is the field that matches the last four digits of the current year, if there is an appostrophy 
                    then assume the year follows the appostrophy. If the date is not parsable then return the word "unknown". Also the input time may
                    be non-military time.
            
                    the date to transform is :\n\n{date_string}\n\n""",
    )

    # Create an LLM chain
    chain = prompt | llm

    # Run the chain to correct the OCR text
    response = chain.invoke({"date_string": date_string})#.run(date_string)
    extractedDate = re.split(r"(\d{4}-\d{2}-\d{2} \d{1,2}:\d{1,2})", response.content)
    return extractedDate[1] if len(extractedDate) > 1 else "unknown"

def save_to_mongo(data_dict):
    """
    Given a dictionary, this function saves the data to a MongoDB database.
    It uses the pymongo library to connect to the database and insert the data.
    """

    from pymongo.mongo_client import MongoClient
    from pymongo.server_api import ServerApi

    mongoUser= os.getenv("MONGODB_USERNAME")
    mongoPass= os.getenv("MONGODB_PASSWORD")
    uri = f"mongodb+srv://{mongoUser}:{mongoPass}@can-sheep.rgm9mzn.mongodb.net/?retryWrites=true&w=majority&appName=can-sheep"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        db = client["can-sheep"]
        db["sheep_transportation"].insert_one(data_dict)
    except Exception as e:
        print(e)