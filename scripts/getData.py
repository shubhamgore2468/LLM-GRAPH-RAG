import asyncio
import json
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup

async def extract_reviews_and_product_info(content, json_data):
    """Parse the page content to extract reviews and product information."""
    soup = BeautifulSoup(content, "html.parser")
    
    # Extract product information (you may need to adjust the selectors based on Amazon's HTML structure)
    product_title = soup.find("span", {"id": "productTitle"})
    product_price = soup.find("span", {"class": "a-price-whole"})
    product_desc = soup.find("div", {"id": "productDescription_feature_div"})
    
    # Extract reviews (you may need to adjust the selectors based on Amazon's HTML structure)
    reviews = soup.find_all("span", {"data-hook": "review-body"})
    
    # Format extracted data
    product_info = {
        "title": product_title.get_text(strip=True) if product_title else "Title not found",
        "price": product_price.get_text(strip=True) if product_price else "Price not found",
        "description": product_desc.get_text(strip=True) if product_desc else "Description not found",
        "reviews": [review.get_text(strip=True) for review in reviews] if reviews else []
    }

    # Safely get the title, using a fallback if it's not available
    title_key = " ".join(product_info.get('title', 'Unknown Product').split(' ')[:3])

    # Add the product info to the dictionary using the title as the key
    json_data[title_key] = product_info

    return json_data

async def crawlAI(url, json_data):
    # Create an instance of AsyncWebCrawler
    async with AsyncWebCrawler(verbose=True) as crawler:
        # Run the crawler on a URL
        result = await crawler.arun(url)

        # Extract reviews and product info from the content
        await extract_reviews_and_product_info(result.html, json_data)

        # Return the accumulated data
        return json_data
