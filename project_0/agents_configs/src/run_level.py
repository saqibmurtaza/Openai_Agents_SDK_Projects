from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled
from dotenv import load_dotenv
from agents.run import RunConfig
import os, asyncio

load_dotenv()

# LLM_RUN LEVEL CONFIG

base_url= os.getenv("BASE_URL")
api_key= os.getenv("API_KEY")
model_name= os.getenv("MODEL_NAME")

print("BASE_URL:", os.getenv("BASE_URL"))
print("API_KEY:", os.getenv("API_KEY"))
print("MODEL_NAME:", os.getenv("MODEL_NAME"))

client= AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
)

model= OpenAIChatCompletionsModel(
    model=model_name,
    openai_client=client
)

config= RunConfig(
    model=model,
    model_provider=client,
    tracing_disabled=True
)

agent: Agent= Agent(
    name= "Assistant",
    instructions="You respond in user_friendly style"
)

result= Runner.run_sync(agent, "What is the weather of Peshawar", run_config=config)
print(result.final_output)

