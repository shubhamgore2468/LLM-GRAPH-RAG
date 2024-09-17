import sys
import os
from dotenv import load_dotenv
import streamlit as st
from src.data_collection.amazonScrapper import scrape
import json

try:
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

        with open('../data/matches.json', 'w') as json_file:
            json.dump(matches, json_file, indent=4)  

        st.stop()

except Exception as e:
    st.write(f"An error occurred: {e}")