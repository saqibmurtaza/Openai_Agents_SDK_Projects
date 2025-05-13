import os  
import gspread  
import asyncio  
from shopping_agent.tools import search_products  
from agents import Runner
from shopping_agent.config_agents import config
from shopping_agent.shopping_agents import shopping_manager

# Print expected path for confirmation  
print("Expected gc.json path:", os.path.abspath("gc.json"))  
GC_JSON_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../gc.json"))  
print("Absolute path to gc.json:", GC_JSON_PATH)  

# Attempt to connect to Google Sheets  
gc = gspread.service_account(GC_JSON_PATH)  
sheet = gc.open("FurnitureProducts").sheet1  
print(sheet.title)  

async def main():  
    # Ensure we call search_products as required by OpenAI Agents SDK  
    try:  
        # Assuming function_tool provides a runner to invoke the recursive function.  
        query = input("Enter your search query: ")
        print(f"Running query: {query}")
        result = await Runner.run(shopping_manager, query, run_config=config)  
        print(result)  
    except Exception as e:  
        print("An error occurred while calling search_products:", str(e))  

if __name__ == "__main__":  
    asyncio.run(main())  