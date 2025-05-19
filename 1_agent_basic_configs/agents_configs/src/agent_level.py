from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os, asyncio, dotenv

load_dotenv()

# LLM_AGENT LEVEL CONFIG

base_url= os.getenv("BASE_URL")
api_key= os.getenv("API_KEY")
model_name= os.getenv("MODEL_NAME")


client= AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
)

set_tracing_disabled(disabled=True)

async def main():
    agent= Agent(
        name= "Assistant",
        instructions="You only respond in haikus.",
        model=OpenAIChatCompletionsModel(
            model=model_name,
            openai_client=client
        )
    )
    result= await Runner.run(agent, "What's the capital of pakistan")
    print(result.final_output)



if __name__ == "__main__":
    asyncio.run(main())
