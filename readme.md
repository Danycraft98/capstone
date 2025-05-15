
## Prerequisite: 
Python 3.11 or better
https://www.python.org/downloads/

pip 
https://pypi.org/project/pip/


## install
```
python -m venv .venv
#unix
source .venv/bin/activate
#windows
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## required .env values

OPENAI_API_KEY=
MONGODB_USERNAME=
MONGODB_PASSWORD=

## to run
to run: 
streamlit run app.py --server.fileWatcherType=none
## references
https://python.langchain.com/docs/how_to/local_llms/

## Install application dependencies
Uninstall