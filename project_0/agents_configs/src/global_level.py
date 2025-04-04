from agents import Agent, OpenAIChatCompletionsModel, Runner, set_default_openai_client
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

# PROBLEMATIC: ISSUE IN CODE

load_dotenv()

# base_url= os.getenv('BASE_URL')
# api_key= os.getenv("API_KEY")
# model_name=os.getenv('MODEL_NAME')

base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
api_key = "AIzaSyDXZrZMgjF826B3YfwdNCN_VcnE2C45ME8"
model_name = "gemini-1.5-flash"

client= AsyncOpenAI(
    base_url=base_url,
    api_key=api_key
)

set_default_openai_client(client)

model= OpenAIChatCompletionsModel(
    model=model_name,
    openai_client=client
)

agent: Agent= Agent(
    name="Assistant",
    instructions="You respond in user_friendly style",
    model=model
)

result= Runner.run_sync(agent, "What is the weather of Peshawar")
print(result.final_output)
