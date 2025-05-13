from agents import function_tool
from typing import List, Dict, Annotated
import os, json, gspread

# Get the project root directory

CREDENTIALS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../gc.json"))


@function_tool
async def search_products(
    query: Annotated[str, "Search term to find products"],
) -> List[Dict]:
    """
    Search for products in the Google Sheet based on query and optional filters.
    
    Args:
        query: Search term to find products
    Returns:
        List of matching products with their details
    """
        
    try:
        # Connect to Google Sheets
        gc = gspread.service_account(filename=CREDENTIALS_PATH)
        sheet = gc.open("FurnitureProducts").sheet1
        
        # Fetch all records; ensure your sheet includes 'name' and 'category' columns
        products = sheet.get_all_records()
        
        # Split the query into individual words for more flexible matching
        query_words = query.lower().split()
        
        # Handle plurals and variations for each word
        query_variations = []
        for word in query_words:
            query_variations.append(word)
            if word.endswith('s'):
                query_variations.append(word[:-1])  # Remove 's' for plural
            else:
                query_variations.append(word + 's')  # Add 's' for singular
        
        # First Search: Match products based on user query and its variations
        matching_products = []
        for p in products:
            product_name = p.get('name', "").lower()
            
            # Check if any of the query words are in the product name
            if any(variation in product_name for variation in query_variations):
                matching_products.append(p)
        
        if not matching_products:
            return json.dumps({"products": [], "recommended_products": [], "message": "No matching products found."})
        
        # Extract all unique categories from matching products
        categories = set(p.get("category", "").strip() for p in matching_products if p.get("category"))
        
        # Second Search: Find more products in any of the matching categories
        recommended_products = []
        for p in products:
            product_category = p.get("category", "").strip()
            if product_category in categories and p not in matching_products:
                recommended_products.append(p)
        
        # Combine results and return JSON
        result = json.dumps({
            "products": matching_products,
            "recommended_products": recommended_products,
            "message": f"Products found successfully in categories: {', '.join(categories)}."
        })
        print(f"SearchTool: {result}")
        return result
    except Exception as e:
        return json.dumps({
            "products": [],
            "recommended_products": [],
            "error": str(e)
        })
