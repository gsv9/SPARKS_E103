import requests
import os
from dotenv import load_dotenv

load_dotenv()

SERP_API_KEY = os.getenv("SERP_API_KEY")
BASE_URL = "https://serpapi.com/search"

def search_products(product_name):
    params = {
        "engine": "google_shopping",
        "q": product_name,
        "hl": "en",
        "gl": "in",
        "api_key": SERP_API_KEY
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    data = response.json()

    results = []

    for item in data.get("shopping_results", []):
        results.append({
            "title": item.get("title"),
            "price": item.get("price"),
            "rating": item.get("rating"),
            "source": item.get("source"),
            "link": item.get("link")
        })

    return results
