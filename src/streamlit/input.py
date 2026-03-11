import asyncio
import os
import sys
import streamlit as st
import json
import logging
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data_processing.preprocess import preprocess_document
from models.createGraph import add_data_to_graph
from inference.langchain_integration import chain

from scripts.getData import crawlAI
# setup_logging()

# st.set_page_config(
#     page_title="Customer Review Analysis",
#     page_icon="📦",
# )
# st.title("Customer Review Analysis")

url1, url2 = None, None

if url1 is None and url2 is None:
    url1 = st.text_input("Enter product URL 1")
    url2 = st.text_input("Enter product URL 2")

    def run_asyncio_task(task):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(task)

    if st.button("Analyze"):
        if not url1 or not url2:
            st.write("Please enter both URLs.")
        else:
            urls = [url1, url2]
            json_data = {}

            try:
                for url in urls:
                    print(f"Crawling URL: {url}")
                    json_res = run_asyncio_task(crawlAI(url, json_data))
                    print("\n")
                
                data_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'crawl_new.json')
                with open(data_path, "w") as json_file:
                    json.dump(json_data, json_file, indent=4)
                # st.write(json_data)
                # st.write("Data Successfully fetched!")
                documents = preprocess_document(json_data)
                add_data_to_graph(documents)
                print("Data successfully fetched and added to the graph.")

                st.write("Ask the chatbot!")
            except Exception as e:
                logging.error(f"An error occurred: {e}")