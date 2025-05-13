# from bs4 import BeautifulSoup
# from agents import function_tool
# from web_scraper_agent.load_env_var import (
#     SHEET_ID,
#     SHEET_NAME,
# )
# import os, requests, gspread



# @function_tool
# def scrape_products(url: str, sheet_id: str = None, sheet_name: str = None) -> list:
#     print(f"🔍 scrape_products called with URL: {url}")
    
#     # Use provided values or fall back to config values
#     sheet_id = SHEET_ID
#     sheet_name = SHEET_NAME
    
#     print(f"Using Sheet ID: {sheet_id}, Sheet Name: {sheet_name}")
    
#     # Scrape the webpage
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
    
#     # Print the HTML structure to help debug
#     print("HTML structure preview:")
#     print(soup.prettify()[:500])  # Print first 500 chars of HTML
    
#     # Let's find all div elements with class attributes to see what's available
#     print("Available div classes:")
#     for div in soup.find_all("div", class_=True):
#         print(f"- {div.get('class')}")
    
#     # Let's also look for product-related elements
#     print("Looking for product-related elements:")
#     for elem in soup.find_all(["div", "section", "article"]):
#         if elem.get("id") and ("product" in elem.get("id").lower() or "item" in elem.get("id").lower()):
#             print(f"Found element with ID: {elem.get('id')}")
    
#     # Try a very simple approach - look for any card-like structures
#     products = []
    
#     # Try with the card class (common in Bootstrap)
#     card_elements = soup.select(".card")
#     print(f"Found {len(card_elements)} card elements")
    
#     if card_elements:
#         for card in card_elements:
#             title = card.select_one(".card-title") or card.select_one("h3") or card.select_one("h4")
#             price = card.select_one(".price") or card.select_one("span")
            
#             products.append({
#                 "name": title.text.strip() if title else "N/A",
#                 "price": price.text.strip() if price else "N/A",
#                 "description": "N/A"
#             })
#     else:
#         # If no cards, try with generic product containers
#         print("No card elements found, trying with generic containers")
        
#         # Look for any div that might contain product info
#         for div in soup.find_all("div"):
#             # Check if this div has both text and some kind of heading
#             headings = div.find_all(["h1", "h2", "h3", "h4", "h5"])
#             if headings and div.text and len(div.text.strip()) > 10:
#                 name = headings[0]
#                 # Look for price-like text (contains $ or numbers)
#                 price_text = None
#                 for p in div.find_all(["p", "span", "div"]):
#                     if p.text and ("$" in p.text or any(c.isdigit() for c in p.text)):
#                         price_text = p
#                         break
                
#                 products.append({
#                     "name": name.text.strip() if name else "N/A",
#                     "price": price_text.text.strip() if price_text else "N/A",
#                     "description": div.text.strip()[:100] + "..." if div.text else "N/A"
#                 })
    
#     print(f"✅ Scraping completed, found {len(products)} products")
    
#     # For testing, just return the scraped data
#     return {"products": products, "sheet_status": "Google Sheets integration skipped for testing"}


from bs4 import BeautifulSoup
from agents import function_tool
import os, requests, gspread
from google.oauth2.service_account import Credentials

@function_tool
def scrape_products(url: str, sheet_id: str = None, sheet_name: str = None) -> dict:
    """
    Scrapes product data from the given URL and saves it to Google Sheets.
    
    Args:
        url: The URL of the webpage to scrape
        sheet_id: The Google Sheet ID where data should be saved
        sheet_name: The name of the sheet tab where data should be saved
        
    Returns:
        A dictionary with product details and status of the Google Sheets operation
    """
    # Import here to avoid circular import issues
    from web_scraper_agent.config_agent import SHEET_ID as CONFIG_SHEET_ID
    from web_scraper_agent.config_agent import SHEET_NAME as CONFIG_SHEET_NAME
    
    # Use provided values or fall back to config values
    sheet_id = sheet_id or CONFIG_SHEET_ID
    sheet_name = sheet_name or CONFIG_SHEET_NAME
    
    # Scrape the webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all product containers
    products = []
    
    # Based on the HTML structure, we're looking for tables-img and tableProduct-content
    product_images = soup.select(".tables-img")
    
    for img_div in product_images:
        # Find the next sibling which should be the product content
        content_div = img_div.find_next_sibling(".tableProduct-content")
        
        if content_div:
            # Extract product name (usually in a heading)
            name_elem = content_div.find(["h2", "h3", "h4", "h5"]) or content_div.find("strong")
            name = name_elem.text.strip() if name_elem else "Unknown Product"
            
            # Extract price (looking for text with $ or numbers)
            price = "N/A"
            for p in content_div.find_all(["p", "span", "div"]):
                if p.text and ("$" in p.text or any(c.isdigit() for c in p.text)):
                    price = p.text.strip()
                    break
            
            # Extract description (any remaining text)
            description = content_div.text.strip()
            if name_elem:
                # Remove the name from the description to avoid duplication
                description = description.replace(name_elem.text.strip(), "", 1).strip()
            
            products.append({
                "name": name,
                "price": price,
                "description": description[:100] + "..." if len(description) > 100 else description
            })
    
    # If no products found with the above approach, try an alternative
    if not products:
        # Look for any container that might have product information
        containers = soup.select(".tableProduct-content")
        
        for container in containers:
            name_elem = container.find(["h2", "h3", "h4", "h5"]) or container.find("strong")
            name = name_elem.text.strip() if name_elem else "Unknown Product"
            
            # Extract other details
            description = container.text.strip()
            if name_elem:
                description = description.replace(name_elem.text.strip(), "", 1).strip()
            
            products.append({
                "name": name,
                "price": "N/A",  # Price might not be easily identifiable
                "description": description[:100] + "..." if len(description) > 100 else description
            })
    
    # Send to Google Sheets
    sheet_status = "No Google Sheets operation attempted"
    
    try:
        # Set up Google Sheets Credentials
        creds_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "gc.json"))
        
        if os.path.exists(creds_path):
            # Define the scope
            scope = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Initialize credentials and client
            credentials = Credentials.from_service_account_file(creds_path, scopes=scope)
            client = gspread.authorize(credentials)
            
            # Open the spreadsheet
            spreadsheet = client.open_by_key(sheet_id)
            
            # Get or create the worksheet
            try:
                sheet = spreadsheet.worksheet(sheet_name)
            except:
                sheet = spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=20)
            
            # Clear existing data
            sheet.clear()
            
            # Add headers
            sheet.append_row(["Product Name", "Price", "Description"])
            
            # Add product data
            for product in products:
                sheet.append_row([
                    product["name"], 
                    product["price"], 
                    product["description"]
                ])
            
            sheet_status = "Data successfully sent to Google Sheets"
        else:
            sheet_status = "Google credentials file not found"
    except Exception as e:
        sheet_status = f"Error sending to Google Sheets: {str(e)}"
    
    return {
        "products": products,
        "count": len(products),
        "sheet_status": sheet_status
    }
