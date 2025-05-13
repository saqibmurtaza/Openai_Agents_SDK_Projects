import chainlit as cl
from shopify_scraper.single_agent import main

@cl.on_message
async def handle_message(message: cl.Message):
    try:
        if "|" not in message.content:
            await cl.Message(
                content="Please provide input in the format:\n\n`<shopify_url> | <google_sheet_url>`"
            ).send()
            return

        shopify_url, sheet_url = map(str.strip, message.content.split("|", 1))

        await cl.Message(content="⏳ Scraping products and saving to Google Sheets...").send()

        # Run your agent
        result = await main(shopify_url, sheet_url)

        # Show result
        await cl.Message(content=f"✅ Done! Output:\n```json\n{result}\n```").send()

    except Exception as e:
        await cl.Message(content=f"❌ Error: {str(e)}").send()
