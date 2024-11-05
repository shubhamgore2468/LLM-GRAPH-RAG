import streamlit as st


st.set_page_config(
    page_title="Customer Review Analysis",
    page_icon="📦",
)
st.title("Customer Review Analysis")

pg = st.navigation([st.Page("streamlit/input.py"), st.Page("streamlit/chatbot.py")])
pg.run()