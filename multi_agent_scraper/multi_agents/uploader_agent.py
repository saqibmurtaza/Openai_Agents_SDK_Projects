# UploaderAgent (optional): Sends final data to Google Sheets.

import gspread
from google.oauth2.service_account import Credentials
import os

def run_uploader_agent(products, sheet_id, sheet_name):
    creds_path = os.path.join(os.getcwd(), "gc.json")
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file(creds_path, scopes=scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key(sheet_id)
    try:
        sheet = spreadsheet.worksheet(sheet_name)
        sheet.clear()
    except:
        sheet = spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=20)

    sheet.append_row(["Product Name", "Price", "Description"])
    for product in products:
        sheet.append_row([product["name"], product["price"], product["description"]])

    return f"Uploaded {len(products)} products to Google Sheets."

# import streamlit as st
# import requests, os
# import pandas as pd
# import re
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# GOOGLE_CREDENTIALS_FILE =  os.path.join(os.getcwd(), "gc.json") 

# # Google Sheets setup (make sure your credentials JSON file is correct)
# SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
# CREDS = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, SCOPE)
# CLIENT = gspread.authorize(CREDS)
# SPREADSHEET = CLIENT.open("Shopify Products")

# # Function to clean Shopify product description HTML
# def clean_html(raw_html):
#     cleanr = re.compile('<.*?>')
#     cleantext = re.sub(cleanr, '', raw_html)
#     return cleantext.strip()

# # Function to fetch products from Shopify collection
# def fetch_products(collection_url):
#     if not collection_url.endswith('.json'):
#         collection_url = collection_url.rstrip('/') + '.json'
#     response = requests.get(collection_url)
#     if response.status_code != 200:
#         return None
#     data = response.json()
#     if "products" not in data:
#         return None
#     products = []
#     for p in data["products"]:
#         products.append({
#             "Title": p["title"],
#             "Price": p["variants"][0]["price"],
#             "Description": clean_html(p.get("body_html", ""))
#         })
#     return products

# # Streamlit UI
# st.title("Shopify Product Scraper")

# urls_input = st.text_area("Enter Shopify Collection URLs (one per line):", height=150)

# if st.button("Fetch & Save to Google Sheets"):
#     urls = [u.strip() for u in urls_input.splitlines() if u.strip()]
#     if not urls:
#         st.warning("Please enter at least one URL.")
#     else:
#         for url in urls:
#             with st.spinner(f"Processing: {url}"):
#                 products = fetch_products(url)
#                 if not products:
#                     st.warning(f"No products found at {url}")
#                     continue
#                 df = pd.DataFrame(products)
#                 sheet_name = url.strip("/").split("/")[-1]  # get collection name
#                 try:
#                     worksheet = SPREADSHEET.worksheet(sheet_name)
#                     SPREADSHEET.del_worksheet(worksheet)
#                 except:
#                     pass
#                 worksheet = SPREADSHEET.add_worksheet(title=sheet_name, rows="100", cols="20")
#                 worksheet.update([df.columns.values.tolist()] + df.values.tolist())
#                 st.success(f"Saved {len(products)} products to tab '{sheet_name}'")
