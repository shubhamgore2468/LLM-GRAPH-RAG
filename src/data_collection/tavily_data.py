from tavily import TavilyClient
import os
from dotenv import load_dotenv
import logging

load_dotenv()

def response_tavily(query):
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(query)
    contents = [item['content'] for item in response['results']]
    logging.info(f"Tavily response: {contents}")
    return " ".join(contents)
