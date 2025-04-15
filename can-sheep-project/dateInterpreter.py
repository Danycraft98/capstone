import re
from datetime import datetime
from typing import Optional

full_months = ["january", "february", "march", "april", "may", "june",
               "july", "august", "september", "october", "november", "december"]

short_months = ["jan", "feb", "mar", "apr", "may", "jun",
                "jul", "aug", "sep", "oct", "nov", "dec"]

full_week_days = ["monday", "tuesday", "wednesday", "thursday",
             "friday", "saturday", "sunday"]

short_week_days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
def interpret_date(departure_date:str, arrivate_date:str  )->dict:

    rtn={}
    # attempt with "Month Day, Year"
    optionalOfDate=attemptMonthOfyearFormat(departure_date)
    if optionalOfDate:
        # If the date string is in the expected format, return the parsed date
        rtn.update({"arrival_date":optionalOfDate}) 
        

    optionalOfDate=attemptMonthOfyearFormat(arrivate_date)
    if optionalOfDate:
        # If the date string is in the expected format, return the parsed date
        rtn.update({"departure_date":optionalOfDate})

    # if we have both fields just return now
    if rtn.get("arrival_date") and rtn.get("departure_date"):
        return rtn

    return rtn

def attemptMonthOfyearFormat(date_string:str)->Optional[tuple]:
    """
    Attempt to parse a date string in the format "Month Day, Year" (e.g., "Jan 10, 2015").
    Returns a tuple containing the month, day, and year as integers.
    """
    import torch
    from transformers import pipeline

    pipe = pipeline("text-generation", 
                    model="TinyLlama/TinyLlama-1.1B-Chat-v0.6", 
                    torch_dtype=torch.bfloat16, device_map="auto"
                    )

    # We use the tokenizer's chat template to format each message - see https://huggingface.co/docs/transformers/main/en/chat_templating
    messages = [
        {"role": "user", "content": f"the date is {date_string}. what is the year?"},
    ]
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.1, top_k=50, top_p=0.95)
    print(outputs[0]["generated_text"])
    print(outputs[0]["generated_text"])







