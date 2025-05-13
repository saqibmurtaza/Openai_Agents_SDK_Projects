###################################
# Code Works without any issues
#####################################

# import requests
# from bs4 import BeautifulSoup

# def fetch_collection_products_json(shop_domain: str, collection_handle: str):
#     """
#     Fetch all products in a Shopify collection via the JSON endpoint,
#     handling pagination (limit=250 per page).
#     Returns a flat list of product dicts.
#     """
#     products = []
#     page = 1
#     while True:
#         url = f"https://{shop_domain}/collections/{collection_handle}/products.json"
#         params = {"limit": 250, "page": page}
#         print(f"Fetching page {page} of collection '{collection_handle}'…")
#         resp = requests.get(url, params=params)
#         resp.raise_for_status()
#         data = resp.json().get("products", [])
#         if not data:
#             break
#         products.extend(data)
#         if len(data) < 250:
#             # no more pages
#             break
#         page += 1
#     return products

# def clean_html(raw_html: str) -> str:
#     """
#     Strip HTML tags from a string using BeautifulSoup.
#     """
#     return BeautifulSoup(raw_html or "", "html.parser").get_text(" ", strip=True)

# def scrape_collection(shop_domain: str, collection_handle: str):
#     """
#     Fetch and print title, price, and cleaned description for each product
#     in the given Shopify collection.
#     """
#     products = fetch_collection_products_json(shop_domain, collection_handle)
#     if not products:
#         print("No products found in this collection.")
#         return

#     for p in products:
#         title = p.get("title", "N/A")
#         # take the first variant’s price
#         price = p.get("variants", [{}])[0].get("price", "N/A")
#         # clean out HTML tags from the description
#         description = clean_html(p.get("body_html", ""))
#         print(f"Title:       {title}")
#         print(f"Price:       {price}")
#         print(f"Description: {description[:100]}{'…' if len(description)>100 else ''}")
#         print("-" * 60)

# if __name__ == "__main__":
#     # === CONFIGURE THESE TWO ===
#     SHOP_DOMAIN      = "maguireshoes.com"   # e.g. "maguireshoes.com"
#     COLLECTION_SLUG  = "sneakers"           # e.g. "sneakers"
#     # ===========================

#     scrape_collection(SHOP_DOMAIN, COLLECTION_SLUG)



# scrape_shopify_collection.py
import requests

def fetch_products_from_collection(collection_url):
    if not collection_url.endswith('.json'):
        collection_url = collection_url.rstrip('/') + '.json'

    response = requests.get(collection_url)
    response.raise_for_status()

    products = response.json().get("products", [])
    results = []
    for product in products:
        title = product["title"]
        price = product["variants"][0]["price"]
        description = product.get("body_html", "")
        results.append((title, price, description))
    return results


import gspread
from oauth2client.service_account import ServiceAccountCredentials

def save_to_google_sheet(data, sheet_name="Shopify Products"):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("your_google_creds.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open(sheet_name).sheet1
    sheet.clear()
    sheet.append_row(["Title", "Price", "Description"])
    for row in data:
        sheet.append_row(list(row))
