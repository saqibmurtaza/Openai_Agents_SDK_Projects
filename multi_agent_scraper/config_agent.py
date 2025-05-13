from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled
from agents.run import RunConfig
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os, asyncio

load_dotenv()
# Load environment variables from null file
BASE_URL= os.getenv("BASE_URL", "")
API_KEY= os.getenv("API_KEY") or ""
MODEL_NAME= os.getenv("MODEL_NAME", "gemini-1.5-flash")
SHEET_ID = os.getenv("SHEET_ID", "")
SHEET_NAME = os.getenv("SHEET_NAME", "tables")

set_tracing_disabled(disabled=True)

client= AsyncOpenAI(
    base_url=BASE_URL,
    api_key=API_KEY,
)

model= OpenAIChatCompletionsModel(
    openai_client=client,
    model=MODEL_NAME,
)

config= RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True,

)
