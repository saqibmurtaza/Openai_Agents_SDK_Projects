from agents import OpenAIChatCompletionsModel, set_tracing_disabled
from agents.run import RunConfig
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")

# Disable tracing for cleaner output
set_tracing_disabled(disabled=True)

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
