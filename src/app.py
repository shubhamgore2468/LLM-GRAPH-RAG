import sys
import os
from dotenv import load_dotenv
import streamlit as st
from data_collection.scrapper import scrape

# Load environment variables from .env file
load_dotenv()

# Add the root directory of your project to sys.path
sys.path.append(os.getenv('PYTHONPATH'))

# Title of the app
st.title("Customer review analysis")

# Adding a button
if st.button("Click Me"):
    st.write("Button clicked!")

# Adding a text input
url1 = st.text_input("Enter product URL 1")
url2 = st.text_input("Enter product URL 2")

if st.button("Analyze"):
    lst = []
    matches = []
    lst.extend([url1, url2])

    for url in lst:
        st.write(f'Scraping URL: {url}')
        matches = scrape(url)
        st.write(matches)
        st.write("END")
        st.write("-----------------------------------------------------------------")

    st.stop()