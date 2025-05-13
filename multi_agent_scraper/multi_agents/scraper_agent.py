# ScraperAgent (multiple): Each one scrapes one URL independently.

from tools.scrape_tool import scrape_page

def run_scraper_agent(url):
    try:
        products = scrape_page(url)
        return {"url": url, "products": products, "count": len(products), "status": "success"}
    except Exception as e:
        return {"url": url, "products": [], "count": 0, "status": f"error: {str(e)}"}
