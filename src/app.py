import asyncio
import os
import sys
import streamlit as st
import json
import logging
from data_processing.preprocess import preprocess_document
from models.createGraph import add_data_to_graph
from inference.langchain_integration import chain

# Set up logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.getData import crawlAI

from logging_config import setup_logging
setup_logging()

st.title("Customer Review Analysis")

# Initialize session state variables
if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False

if "messages" not in st.session_state:
    st.session_state.messages = []

# Only show URL input section if analysis is not complete
if not st.session_state.analysis_complete:
    url1 = st.text_input("Enter product URL 1")
    url2 = st.text_input("Enter product URL 2")

    def run_asyncio_task(task):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(task)

    if st.button("Analyze"):
        if not url1 or not url2:
            st.warning("Please enter both URLs.")
        else:
            urls = [url1, url2]
            json_data = {}

            try:
                with st.spinner("Crawling URLs and processing data..."):
                    for url in urls:
                        logging.info(f"Crawling URL:")
                        json_res = run_asyncio_task(crawlAI(url, json_data))
                        # not using tavily yet, crawl4ai in scripts/getData.py
                        logging.info("\n")

                    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'crawl_new.json')
                    with open(data_path, "w") as json_file:
                        json.dump(json_data, json_file, indent=4)

                    st.success("Data Successfully fetched!")

                    # Pass the in-memory JSON object instead of file path
                    documents = preprocess_document(json_data)
                    add_data_to_graph(documents)

                    # Mark analysis as complete
                    st.session_state.analysis_complete = True
                    st.success("Analysis complete! You can now ask questions about the products.")
                    st.rerun()

            except Exception as e:
                logging.error(f"An error occurred: {e}")
                st.error(f"An error occurred: {e}")

# Chat section - only available after analysis is complete
if st.session_state.analysis_complete:
    st.markdown("---")
    st.subheader("Ask questions about the analyzed products:")

    # Add a reset button
    if st.button("Start New Analysis", type="secondary"):
        st.session_state.analysis_complete = False
        st.session_state.messages = []  # Clear chat history
        st.rerun()

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask something about the products..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            with st.spinner("Processing your question..."):
                # Call the RAG model with the prompt
                response = chain.invoke({"question": prompt})

                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response})

                # Display assistant response
                with st.chat_message("assistant"):
                    st.markdown(response)

        except Exception as e:
            error_msg = f"An error occurred while processing your question: {e}"
            logging.error(error_msg)
            st.error(error_msg)
            # Add error to chat history
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

else:
    st.info("Please enter URLs and click 'Analyze' to process the data before asking questions.")