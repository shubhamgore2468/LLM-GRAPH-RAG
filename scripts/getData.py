import os
import logging
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

def crawlAI(url, json_data):
    """Extract product info from a URL using Tavily's extract API."""
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    # Use Tavily search to get product info from the URL
    search_response = client.search(url, max_results=5)
    search_results = search_response.get("results", [])

    if not search_results:
        logging.warning(f"Tavily search returned no results for {url}")
        key = f"product_{len(json_data) + 1}"
        json_data[key] = {"title": key, "description": "", "about": "", "reviews": []}
        return json_data

    title = search_results[0].get("title", "")
    title_key = " ".join(title.split()[:3]) if title else f"product_{len(json_data) + 1}"
    description = " ".join(item["content"] for item in search_results)

    json_data[title_key] = {
        "title": title or title_key,
        "description": description,
        "about": "",
        "reviews": [],
    }

    logging.info(f"Extracted product: {title_key}")
    return json_data
