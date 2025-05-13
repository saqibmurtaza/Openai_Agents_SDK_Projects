##############################################################
# This script fetches product data from a Shopify collection, saves it to a Google Sheet,
# and displays it in a Streamlit app.
# CODE RUNS WITOUT ANY ERRORS
###################################################################

# import requests, os
# import gspread
# import streamlit as st
# import pandas as pd
# from oauth2client.service_account import ServiceAccountCredentials
# from bs4 import BeautifulSoup

# # CONFIGURATION
# SHOPIFY_COLLECTION_URL = "https://maguireshoes.com/collections/sneakers"
# GOOGLE_SHEET_NAME = "Shopify Products"
# GOOGLE_CREDENTIALS_FILE =  os.path.join(os.getcwd(), "null")  # Replace with your actual JSON key file

# # STEP 1: Fetch products from Shopify JSON endpoint
# def fetch_products_from_collection(collection_url):
#     if not collection_url.endswith(".json"):
#         collection_url = collection_url.rstrip("/") + "/products.json"

#     response = requests.get(collection_url)
#     response.raise_for_status()

#     products = response.json().get("products", [])
#     results = []
#     for product in products:
#         title = product["title"]
#         price = product["variants"][0]["price"]
#          # Clean HTML from description
#         raw_html = product.get("body_html", "")
#         soup = BeautifulSoup(raw_html, "html.parser")
#         description = soup.get_text(separator=" ", strip=True)
        
#         results.append((title, price, description))
#     return results

# # STEP 2: Save to Google Sheet
# def save_to_google_sheet(data, sheet_name=GOOGLE_SHEET_NAME):
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, scope)
#     client = gspread.authorize(creds)

#     sheet = client.open(sheet_name).sheet1
#     sheet.clear()
#     sheet.append_row(["Title", "Price", "Description"])
#     for row in data:
#         sheet.append_row(list(row))

# # STEP 3: Load data from Google Sheets into DataFrame
# def load_data_from_google_sheet(sheet_name=GOOGLE_SHEET_NAME):
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, scope)
#     client = gspread.authorize(creds)
#     sheet = client.open(sheet_name).sheet1
#     data = sheet.get_all_records()
#     return pd.DataFrame(data)

# # MAIN SCRIPT
# if __name__ == "__main__":
#     st.title("🛍️ Shopify Sneaker Collection Viewer")

#     with st.spinner("Fetching products from Shopify..."):
#         try:
#             products = fetch_products_from_collection(SHOPIFY_COLLECTION_URL)
#             save_to_google_sheet(products)
#             st.success(f"Fetched and saved {len(products)} products to Google Sheets!")
#         except Exception as e:
#             st.error(f"Error: {e}")

#     st.subheader("Products Table")
#     df = load_data_from_google_sheet()
#     search = st.text_input("Search by product title")

#     if search:
#         filtered_df = df[df["Title"].str.contains(search, case=False)]
#     else:
#         filtered_df = df

#     st.dataframe(filtered_df, use_container_width=True)


##############################################################
# This script fetches product data from a Shopify collection, saves it to a Google Sheet,
# and displays it in a Streamlit app.
# FOLLOWING CODE RUNS WITOUT ANY ERRORS
###################################################################

import streamlit as st
import requests, os
import pandas as pd
import re
from urllib.parse import urlparse
from google.oauth2.service_account import Credentials
import gspread
from bs4 import BeautifulSoup


GOOGLE_CREDENTIALS_FILE = os.path.join(os.getcwd(), "null")

# Authenticate with Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE, scopes=scope)
client = gspread.authorize(creds)

# Streamlit UI
st.title("Shopify Collection Scraper to Google Sheets")

urls_input = st.text_area("Enter product page URLs (one per line):", height=200)
urls = [url.strip() for url in urls_input.splitlines() if url.strip()]

sheet_url = st.text_input("Enter your Google Sheet URL")
go_button = st.button("Scrape and Save")

def extract_collection_handle(url):
    path = urlparse(url).path
    match = re.search(r"/collections/([^/?#]+)", path)
    return match.group(1) if match else "sheet"

def fetch_products_from_collection(url):
    collection_handle = extract_collection_handle(url)
    json_url = f"https://{urlparse(url).netloc}/collections/{collection_handle}/products.json"
    try:
        response = requests.get(json_url)
        response.raise_for_status()
        return response.json().get("products", [])
    except Exception as e:
        st.error(f"Error fetching from {url}: {e}")
        return []

def extract_product_data(product):
    title = product.get("title", "")
    price = product.get("variants", [{}])[0].get("price", "")
    
    # Clean HTML from description
    # Use BeautifulSoup to parse the HTML and extract text
    description_html = product.get('body_html', '')
    soup = BeautifulSoup(description_html, "html.parser")
    description = soup.get_text(separator=" ", strip=True)

    return {
        "Title": title,
        "Price": price,
        "Description": description,
    }

def save_to_gsheet(sheet_url, tab_name, data):
    try:
        spreadsheet = client.open_by_url(sheet_url)
        try:
            worksheet = spreadsheet.worksheet(tab_name)
            spreadsheet.del_worksheet(worksheet)
        except:
            pass
        worksheet = spreadsheet.add_worksheet(title=tab_name, rows="100", cols="20")
        df = pd.DataFrame(data)
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    except Exception as e:
        st.error(f"Google Sheets error: {e}")

if go_button:
    if not urls:
        st.warning("Please enter at least one URL.")
    elif not sheet_url:
        st.warning("Please enter your Google Sheet URL.")
    else:
        for url in urls:
            st.write(f"Fetching products from: {url}")
            products = fetch_products_from_collection(url)
            if not products:
                st.warning(f"⚠️ No products found at {url}")
                continue
            product_data = [extract_product_data(p) for p in products]
            tab_name = extract_collection_handle(url)[:100]  # Sheet name max length = 100
            save_to_gsheet(sheet_url, tab_name, product_data)
            st.success(f"✅ Saved {len(product_data)} products to sheet tab: {tab_name}")
