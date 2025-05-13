from agents import Agent, Runner
from shopify_scraper.tools.shopify_scrapper import scrape_shopify_collection, extract_product_data
from shopify_scraper.tools.save_to_google import save_to_sheet
from shopify_scraper.config_agent import config


# Shopify scraping agent
shopify_agent = Agent(
    name="shopify_agent",
    instructions="""You are a Shopify product scraping specialist.

    When given a shopify URL and as sheet URL, you must:
    1. Use scrape_shopify_collection to get the product data
    2. Return ONLY the scraped product data as a JSON array
    3. Use save_to_sheet to write the data
    3. Save data to Google Sheet using tool save_to_sheet
    
    Do not add any extra text or explanations.
    Do not ask for additional functionality.
    Just return the raw product data array.
    """,
    tools=[scrape_shopify_collection, extract_product_data, save_to_sheet],
    
)

# 
# Example values - replace with actual URLs
shopify_url = "https://maguireshoes.com/collections/sneakers"
sheet_url = "https://docs.google.com/spreadsheets/d/1DtZXL0gVeU-kr4WpUcBpmQJr-h9-SBgYY9Lzb5pxAoY/edit?gid=0#gid=0"

# New main execution function for testing or direct use
async def main(shopify_url, sheet_url):
   
    input_data = {
        "shopify_url": shopify_url,
        "sheet_url": sheet_url,
    } 
    import json

    stringify= json.dumps(input_data)
    # Print for debugging
    print(f"Starting workflow with input: {stringify}")
    
    # Run the triage agent with the input
    result = await Runner.run(
        shopify_agent, 
        input=stringify, 
        run_config=config)
    
    return result

if __name__ == "__main__":
    import asyncio
    final_output= asyncio.run(main(shopify_url, sheet_url))
    print(final_output)





# Data writer agent
# data_writer_agent = Agent(
#     name="data_writer_agent",
#     instructions="""You are a Google Sheets data writing specialist.

#     When given product data and a sheet URL, you must:
#     1. Use save_to_sheet to write the data
#     2. Return ONLY the success/failure message
    
#     Do not add any extra text or explanations.
#     Do not modify the input data.
#     Just save and return the status message.
#     """,
#     tools=[save_to_sheet],
#     handoff_description="Saves product data to Google Sheets"
# )

# # Triage agent
# triage_agent = Agent(
#     name="Shopify Collection Scraper",
#     instructions="""You coordinate scraping and saving Shopify product data.
    
#     Follow these steps exactly:
#     1. Parse the input JSON to get shopify_url and sheet_url
#     2. Hand off to shopify_agent with ONLY the shopify_url
#     3. Take the product data array returned by shopify_agent
#     4. Hand off to data_writer_agent with both the product data and sheet_url
#     5. Return the final save status message
    
#     IMPORTANT: When handing off to data_writer_agent, you MUST include:
#       - The sheet_url as a string
#       - The products data as a list of dictionaries
#       - Use the format: {"sheet_url": "...", "products": [...]}
    
#     Do not modify or filter the data between agents.
#     Do not add extra explanations or text.
#     Just coordinate the data flow between agents.
#     """,
#     handoffs=[shopify_agent, data_writer_agent]
# )
