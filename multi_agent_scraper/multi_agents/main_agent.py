# ## Responsibilities of main_agent.py
# # Calls scraper agents in a loop
# # Aggregates results
# # Optionally uploads to Google Sheets
# # Returns a structured result object for use in the frontend or logs


from multi_agents.aggregator_agent import run_aggregator_agent
from multi_agents.scraper_agent import run_scraper_agent
from multi_agents.uploader_agent import run_uploader_agent
from config_agent import SHEET_ID
from urllib.parse import urlparse
import re

# def run_main_agent(urls: list[str], upload_to_sheets: bool = True) -> dict:
#     if not urls:
#         return {"error": "No URLs provided"}

#     # 1. Scrape each URL using scraper agent
#     # scraped_results = [run_scraper_agent(url) for url in urls]
#     scraped_results = []

#     for url in urls:
#         tab_name = url_to_sheet_name(url)
#         result = run_scraper_agent(url)
#         upload_status = run_uploader_agent(result["products"], SHEET_ID, tab_name)
#         result["sheet_name"] = tab_name
#         result["upload_status"] = upload_status
#         scraped_results.append(result)


#     # 2. Aggregate the product data
#     all_products = run_aggregator_agent(scraped_results)

#     # 3. Upload if needed
#     sheet_status = "Skipping Google Sheets upload"
#     if upload_to_sheets and all_products:
#         sheet_status = run_uploader_agent(all_products, SHEET_ID)

#     # return {
#     #     "total_products": len(all_products),
#     #     "sheet_status": sheet_status,
#     #     "scraped_details": scraped_results,
#     #     "aggregated_products": all_products
#     # }
#     return {
#     "total_products": sum([r["count"] for r in scraped_results]),
#     "scraped_details": scraped_results
#     }


# # Helper function to generate a sheet name from the URL
# def url_to_sheet_name(url):
#     path = urlparse(url).path
#     last_segment = path.strip("/").split("/")[-1]
#     base = re.sub(r'\W+', '_', last_segment).strip("_")
#     return base or "Sheet"

# agents/main_agent.py

def url_to_sheet_name(url: str) -> str:
    path = urlparse(url).path
    last_segment = path.strip("/").split("/")[-1]
    base = re.sub(r'\W+', '_', last_segment).strip("_")
    return base or "Sheet"

def run_main_agent(urls: list[str], upload_to_sheets: bool = True) -> dict:
    if not urls:
        return {"error": "No URLs provided"}

    scraped_results = []

    for url in urls:
        sheet_name = url_to_sheet_name(url)
        result = run_scraper_agent(url)
        result["sheet_name"] = sheet_name

        if upload_to_sheets and result["status"] == "success":
            status = run_uploader_agent(result["products"], SHEET_ID, sheet_name)
            result["upload_status"] = status
        else:
            result["upload_status"] = "Upload skipped or scraping failed."

        scraped_results.append(result)

    return {
        "total_products": sum([r["count"] for r in scraped_results if r["status"] == "success"]),
        "scraped_details": scraped_results
    }
