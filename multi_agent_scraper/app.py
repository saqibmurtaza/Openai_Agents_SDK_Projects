import streamlit as st
from multi_agents.main_agent import run_main_agent

st.set_page_config(page_title="Multi-Agent Web Scraper", layout="wide")
st.title("🕸️ Multi-Agent Web Scraper")

# Input: List of URLs
urls_input = st.text_area("Enter product page URLs (one per line)", height=200)
urls = [url.strip() for url in urls_input.splitlines() if url.strip()]

# Optional: Upload toggle
upload = st.checkbox("Upload to Google Sheets", value=True)

if st.button("Scrape and Process"):
    if not urls:
        st.error("Please enter at least one URL.")
    else:
        with st.spinner("Running main agent..."):
            result = run_main_agent(urls, upload_to_sheets=upload)

        if "error" in result:
            st.error(result["error"])
        else:
            st.success(f"✅ Scraped {result['total_products']} products")
            # st.info(f"📤 Sheet Upload Status: {result['sheet_status']}")
            for detail in result["scraped_details"]:
                st.markdown(f"📄 **{detail['sheet_name']}** - {detail['upload_status']} ({detail['count']} products)")
            st.subheader("Aggregated Products")
            # st.dataframe(result["aggregated_products"])
            first_page = next((d for d in result["scraped_details"] if d["status"] == "success"), None)
            if first_page:
                st.dataframe(first_page["products"])
            else:
                st.warning("No products to display.")

            st.subheader("Detailed Results per URL")
            for res in result["scraped_details"]:
                st.markdown(f"**URL**: {res['url']}")
                st.write(f"Status: {res['status']}, Products Found: {res['count']}")
