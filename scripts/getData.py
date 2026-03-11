from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup
from scripts.tavily_search import response_tavily

async def extract_reviews_and_product_info(content, json_data):
    """Parse the page content to extract reviews and product information."""
    soup = BeautifulSoup(content, "html.parser")
    
    product_title = soup.find("span", {"id": "productTitle"})
    product_price = soup.find("span", {"class": "a-price-whole"})
    product_desc = soup.find("div", {"id": "productDescription_feature_div"})
    
    reviews = soup.find_all("span", {"data-hook": "review-body"})
    
    title_text = product_title.get_text(strip=True) if product_title else None

    product_info = {
        "title": title_text or "Unknown Product",
        "price": product_price.get_text(strip=True) if product_price else "Price not found",
        "description": product_desc.get_text(strip=True) if product_desc else "Description not found",
        "reviews": [review.get_text(strip=True) for review in reviews] if reviews else []
    }

    # Use URL as fallback key to avoid collision when title is missing
    title_key = " ".join(product_info['title'].split()[:3]) if title_text else f"product_{len(json_data) + 1}"

    if title_text:
        tavily_response = response_tavily(title_text)
        product_info['description'] += f" {tavily_response}"
    

    json_data[title_key] = product_info

    return json_data

async def crawlAI(url, json_data):
    async with AsyncWebCrawler(verbose=False) as crawler:
        result = await crawler.arun(url)

        await extract_reviews_and_product_info(result.html, json_data)

        return json_data
