
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from web_scraper_agent.tools.scrape_tool import scrape_products
from openai import AsyncOpenAI
from agents.run import RunConfig
from dotenv import load_dotenv
import os, asyncio

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = os.getenv("BASE_URL", "")
API_KEY = os.getenv("API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "")
SHEET_ID = os.getenv("SHEET_ID", "")
SHEET_NAME = os.getenv("SHEET_NAME", "livingroom")

# Disable tracing for cleaner output
set_tracing_disabled(disabled=True)

# Initialize the agent
agent = Agent(
    name="WebScraperAgent",
    instructions="""You are a helpful agent that scrapes product data from webpages and sends it to Google Sheets.
    When asked to scrape a webpage, use the scrape_products tool with the URL, sheet_id, and sheet_name.
    After scraping, provide a summary of what was found and whether the data was successfully sent to Google Sheets.""",
    tools=[scrape_products],
)

# Set up OpenAI client and model
client = AsyncOpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)

model = OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=client,
)

config = RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

# Main function to run the agent
async def main():
    print("Starting the web scraper agent...")
    
    # Create a prompt with all necessary information
    prompt = f"""
    Please scrape living room products from https://saqibmurtaza.github.io/Jawad_Responsive_Website/livingroom.html 
    and save them to my Google Sheet with ID '{SHEET_ID}' and sheet name '{SHEET_NAME}'.
    """
    
    # Run the agent
    result = await Runner.run(
        agent,
        prompt,
        run_config=config
    )
    
    print("Agent execution completed.")
    print("Final output:", result.final_output)
    return result.final_output

# Run the agent when the script is executed directly
if __name__ == "__main__":
    try:
        output = asyncio.run(main())
        print("\nFull output from main function:")
        print(output)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
