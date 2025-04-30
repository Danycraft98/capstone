import json
import logging
import streamlit as st
from datetime import datetime
from PIL import Image

from ocr import ocr
from ocr import functions

logger = logging.getLogger(__name__)


# For elements to be displayed in the sidebar, we need to add the sidebar element in the widget.
# We create a upload input field for users to enter their API key.
uploaded_file = st.sidebar.file_uploader("Choose an image file")
if uploaded_file:
    image=Image.open(uploaded_file)
    # not thread safe
    image.save("./tmp/uploaded_file.png")
    # file_content= ocr.get_text("./tmp/uploaded_file.png")
    file_content= ocr.get_encoded_file("./tmp/uploaded_file.png")
    st.sidebar.image(image, caption='Uploaded Image', use_container_width=True)


st.sidebar.markdown("---")


# Let's add some info about the app to the sidebar.

st.sidebar.write(
    """

App created by [Charly Wargnier](https://twitter.com/DataChaz) using [Streamlit](https://streamlit.io/)🎈 and [HuggingFace](https://huggingface.co/inference-api)'s [Distilbart-mnli-12-3](https://huggingface.co/valhalla/distilbart-mnli-12-3) model.

"""
)

st.title("Sheep Transportation Tracking")
MainTab, InfoTab = st.tabs(["Main", "Info"])

with InfoTab:

    st.subheader("What is Streamlit?")
    st.markdown(
        "[Streamlit](https://streamlit.io) is a Python library that allows the creation of interactive, data-driven web applications in Python."
    )

    st.subheader("Resources")
    st.markdown(
        """
    - [Streamlit Documentation](https://docs.streamlit.io/)
    - [Cheat sheet](https://docs.streamlit.io/library/cheatsheet)
    - [Book](https://www.amazon.com/dp/180056550X) (Getting Started with Streamlit for Data Science)
    """
    )

    st.subheader("Deploy")
    st.markdown(
        "You can quickly deploy Streamlit apps using [Streamlit Community Cloud](https://streamlit.io/cloud) in just a few clicks."
    )


with MainTab:

    # Then, we create a intro text for the app, which we wrap in a st.markdown() widget.

    if uploaded_file:
        logging.info(f"Started extracting process at: {datetime.now()}")
        data_dict = functions.translate_text(file_content)
        logging.info(f"extract text from image {data_dict}")
        for key in data_dict:
            if isinstance(data_dict[key], list):
                data_dict[key] = " ".join(data_dict[key])

        st.table(data_dict)
        possibe_dates=functions.parse_dates(data_dict)
        st.table(possibe_dates)
        logging.info(f"Finished extracting process at: {datetime.now()}")

    else:
        st.write("")
        st.markdown("""Upload a scanned form to get the results""")
        st.write("")
