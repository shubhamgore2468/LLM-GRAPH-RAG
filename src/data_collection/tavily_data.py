from tavily import TavilyClient
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Step 1. Instantiating your TavilyClient
def response_tavily(query):
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    # Step 2. Executing a search query using the input string
    response = tavily_client.search(query)

    # Step 3. Extracting the content from the search results
    contents = [item['content'] for item in response['results']]

    # Join the contents into a single string
    return " ".join(contents)