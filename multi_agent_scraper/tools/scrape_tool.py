from bs4 import BeautifulSoup
import requests

def detect_and_extract_products(html):
    soup = BeautifulSoup(html, "html.parser")
    products = []

    # Update selector to match Shopify product cards
    product_cards = soup.select(".grid__item, .product-card, .product-item")

    for card in product_cards:
        # Extract product name
        name_tag = card.select_one("a.full-unstyled-link, .card__heading, h2, h3")
        name = name_tag.text.strip() if name_tag else "N/A"

        # Extract price (skip strike-throughs if both original and discounted prices are present)
        price_tag = card.select_one(".price-item--sale, .price-item--regular, .price")
        price = price_tag.text.strip() if price_tag else "N/A"

        # Try to get a meaningful description from product meta (if available)
        desc_container = card.select_one(".card__content, .product-card__content")
        raw_desc = desc_container.get_text(separator=" ", strip=True) if desc_container else ""
        
        # Remove irrelevant text
        irrelevant_phrases = ["Quick View", "Sale", "15%", "Add to cart"]
        for phrase in irrelevant_phrases:
            raw_desc = raw_desc.replace(phrase, "")
        description = raw_desc.strip()
        description = description[:200] + "..." if len(description) > 200 else description

        products.append({
            "name": name,
            "price": price,
            "description": description
        })

    return products

def scrape_page(url):
    response = requests.get(url)
    response.raise_for_status()
    html = response.text
    return detect_and_extract_products(html)
