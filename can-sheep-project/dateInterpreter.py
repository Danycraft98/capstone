import arrow
import re
from datetime import datetime
from typing import Optional
# from dateutil import parser
# from dateutil.relativedelta import relativedelta
# from dateutil.parser import parse
# from dateutil.tz import tzlocal
# from dateutil.tz import tzutc          
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
    try:
        # Attempt to parse the date string
        parsed_date = datetime.strptime(date_string, "%b %d, %Y")
        return f"{parsed_date.year:02d}-{parsed_date.month:02d}-{parsed_date.day:02d}"
    except ValueError:
        # If parsing fails, return None
        return None



