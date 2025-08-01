import streamlit as st
import random
import time
from inference.langchain_integration import process_prompt

# Streamed response emulator
def response_generator(response):
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response using the language model
    try:
        st.write("Processing prompt...")
        response = process_prompt(prompt)
    except Exception as e:
        response = f"An error occurred while processing the prompt: {e}"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.write_stream(response_generator(response))
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})