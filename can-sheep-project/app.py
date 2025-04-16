import streamlit as st
from PIL import Image
from ocr import ocr
# For elements to be displayed in the sidebar, we need to add the sidebar element in the widget.
# We create a upload input field for users to enter their API key.
uploaded_file = st.sidebar.file_uploader("Choose an image file")
if uploaded_file:
    image=Image.open(uploaded_file)
    # not thread safe
    image.save("./temp_file_dir/uploaded_file.png")
    text_from_scan= ocr.get_text("./temp_file_dir/uploaded_file.png")
    st.sidebar.image(image, caption='Uploaded Image', use_column_width=True)


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
        st.write(text_from_scan)

        if st.button("Clear Text"):
            text_from_scan = ""  # Reset the text
    else:
        st.write("")
        st.markdown("""Upload a scanned form and press submit to get the results""")
        st.write("")

    # Now, we create a form via `st.form` to collect the user inputs.

    # All widget values will be sent to Streamlit in batch.
    # It makes the app faster!
    