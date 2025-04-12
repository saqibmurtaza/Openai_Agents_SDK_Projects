from agents import function_tool
from typing import List, Dict, Optional, Annotated
import os, json, gspread

# Get the project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
CREDENTIALS_PATH = os.path.join(PROJECT_ROOT, "null")




@function_tool
async def search_products(
    query: Annotated[str, "Search term to find products"],
    category: Annotated[str, "Optional category to filter products"] = "",
    max_price: Annotated[float, "Optional maximum price filter"] = 0.0
) -> List[Dict]:

    """
    Search for products in the Google Sheet based on query and optional filters.    
    Args:
        query: Search term to find products
        category: Optional category to filter products
        max_price: Optional maximum price filter
    
    Returns:
        List of matching products with their details
    """
        
    try:
        # Connect to Google Sheets
        gc = gspread.service_account(filename=CREDENTIALS_PATH)
        sheet = gc.open("FurnitureProducts").sheet1
        
        # Fetch all records; ensure your sheet includes 'name' and 'category' columns
        products = sheet.get_all_records()
        
        # 🔹 Handle plurals and variations
        query_variations = [query.lower()]
        if query.lower().endswith('s'):
            query_variations.append(query.lower()[:-1])  # Remove 's' for plural
        else:
            query_variations.append(query.lower() + 's')  # Add 's' for singular
        
        # 🔹 First Search: Match products based on user query and its variations
        matching_products = []
        for p in products:
            product_name = p.get('name', "").lower()
            for variation in query_variations:
                if variation in product_name:
                    matching_products.append(p)
                    break
        
        if not matching_products:
            return json.dumps({"products": [], "recommended": [], "message": "No matching products found."})
        
        # 🔹 Extract all unique categories from matching products
        categories = set(p.get("category", "").strip() for p in matching_products if p.get("category"))
        
        # 🔹 Second Search: Find more products in any of the matching categories
        recommended_products = []
        for p in products:
            product_category = p.get("category", "").strip()
            if product_category in categories and p not in matching_products:
                recommended_products.append(p)
        
        # 🔹 Combine results and return JSON
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
            "recommended": [],
            "error": str(e)
        })

