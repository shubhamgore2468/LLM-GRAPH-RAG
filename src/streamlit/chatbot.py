import streamlit as st
from inference.langchain_integration import chain



prompt = st.chat_input("Say something")
print(f"Prompt: {prompt}")

# Needs to make call to the model
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")
    try:
        # Call the RAG model with the prompt
        response = chain.invoke({"question": prompt})
        st.write(response)
    except Exception as e:
        st.write(f"An error occurred while invoking the chain: {e}")
else:
    st.write("Prompt is empty or None.")