import os
import logging
import streamlit as st
from datetime import datetime
from PIL import Image

from ocr import ocr
from ocr import functions

logger = logging.getLogger(__name__)

data_dict = {}
# For elements to be displayed in the sidebar, we need to add the sidebar element in the widget.
# We create a upload input field for users to enter their API key.
st.session_state["clearActive"]=False

uploaded_file = st.sidebar.file_uploader("Choose an image file",accept_multiple_files=False)
if uploaded_file is not None and uploaded_file.file_id not in st.session_state:
    st.session_state[uploaded_file.file_id] = True
    image=Image.open(uploaded_file)


    localFileName= f"./tmp/uploaded_file_{uploaded_file.file_id}.png"
    st.session_state["clearActive"]=True
    st.session_state["localFileName"] = localFileName

    file_path = os.path.join(os.getcwd(), localFileName)
    image.save(file_path)

    file_content= ocr.get_encoded_file(file_path)
    st.sidebar.image(image, caption='Uploaded Image', use_container_width=True)

    logging.info(f"Started extracting process at: {datetime.now()}")
    current_date = datetime.now().strftime("%Y-%m-%d")
    # current_date = '2025-04-30'
    if "data_dict" not in st.session_state:
        data_dict = functions.translate_text(file_content,current_date)
        for key in data_dict:
            if isinstance(data_dict[key], list):
                data_dict[key] = " ".join(data_dict[key])
        st.session_state["data_dict"] = data_dict
        st.session_state["possible_dates"] = functions.parse_dates(data_dict)
        logging.info(f"extract text from image {data_dict}")

st.sidebar.markdown("---")


# Let's add some info about the app to the sidebar.

st.sidebar.write(
    """

App created by Matin Mazid and Daniel Lee using [Streamlit](https://streamlit.io/)🎈 and [OpenAI](https://platform.openai.com/docs/overview)'s gpt-4 model.

"""
)

st.title("Sheep Transportation Tracking")
MainTab, InfoTab = st.tabs(["Main", "Info"])

with InfoTab:
    st.subheader("What is Sheep Transportation Tracking?")
    st.markdown(
        "[Sheep Transportation Tracking](https://streamlit.io) is a web-based tool designed to monitor and manage the movement of sheep between farms, markets, and facilities. Built using Streamlit, it provides an intuitive interface for farmers, transport coordinators, and agricultural regulators to track transportation events, ensure animal welfare compliance, and analyze trends in livestock movement."
    )

    st.subheader("Features")
    st.markdown(
        """
    - Interactive Dashboard: Visualize sheep transport activity over time and across regions.
    - Log Management: Add, edit, or remove transportation entries with detailed metadata (date, origin, destination, etc.).
    - Search & Filter: Quickly find specific records based on farm name, animal count, or transport date.
    - Compliance Insights: Identify gaps in transport procedures and stay aligned with animal welfare regulations.
    """
    )

    st.subheader("Learn More")
    st.markdown("""To explore more about the underlying research and objectives, visit the [CanSheep project](https://www.cansheep.ca/)""")


with MainTab:

    # Then, we create a intro text for the app, which we wrap in a st.markdown() widget.
    # if uploaded_file is None:

    doClear=st.button("clear",disabled=not st.session_state["clearActive"])

    if doClear:
        os.remove(st.session_state["localFileName"])
        st.session_state.clear()

    if "data_dict" not in st.session_state:
        st.write("")
        st.markdown("""Upload a scanned form to get the results""")
        st.write("")

    else :
        st.subheader("Extracted Data")
        st.table(st.session_state["data_dict"])
        possibe_dates = st.session_state["possible_dates"]
        st.subheader("Interpreted Date and Time")
        st.table(possibe_dates)
        logging.info(f"Finished extracting process at: {datetime.now()}")
        saveMe=st.button("Save to MongoDB")
        if saveMe:
            functions.save_to_mongo(st.session_state["data_dict"])
            st.success("Data saved to MongoDB successfully!")
            os.remove(st.session_state["localFileName"])
            st.balloons()
        else:
            st.write("Data not saved to MongoDB") 

