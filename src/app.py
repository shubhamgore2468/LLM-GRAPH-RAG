import asyncio
import os
import sys
import streamlit as st
import json
# from models.langchain_integration import chain

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.getData import crawlAI

st.set_page_config(
    page_title="Customer Review Analysis",
    page_icon="📦",
)
st.title("Customer Review Analysis")

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
            
            with open("../data/crawl_new.json", "w") as json_file:
                json.dump(json_data, json_file, indent=4)
            st.write("Data Successfully fetched!")            

        except Exception as e:
            st.write(f"An error occurred: {e}")

prompt = st.chat_input("Say something")
print(prompt)

# Needs to make call to the model
# chain.invoke({"question": prompt})


if prompt:
    st.write(f"User has sent the following prompt: {prompt}")