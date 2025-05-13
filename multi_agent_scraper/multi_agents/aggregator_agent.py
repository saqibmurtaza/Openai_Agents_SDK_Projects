# AggregatorAgent: Merges and de-duplicates results.

def run_aggregator_agent(scraped_results):
    all_products = []
    for result in scraped_results:
        if result["status"] == "success":
            all_products.extend(result["products"])
    return all_products
