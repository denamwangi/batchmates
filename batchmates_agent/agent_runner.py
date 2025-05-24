import asyncio
import os
from .constants import (
    MODEL_GPT_40,
    SESSION_ID,
    APP_NAME,
    USER_ID,
)
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from .agent import root_agent
import warnings
import logging

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

model = MODEL_GPT_40
cheap_model = MODEL_GPT_40
postgres_url = "postgresql://denamwangi:mypassword@localhost:5432/rcdb"


def get_prompt():
    with open("./rcdb_agent_instructions.txt", "r") as f:
        prompt = f.read()
        return prompt


def get_agent_async():
    return root_agent


async def call_agent_async(query: str, runner, user_id, session_id):
    print(f"\n >>> User Query: {query}")

    content = types.Content(role="user", parts=[types.Part(text=query)])
    final_response_text = "Agent did not produce any results sorry"
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=content
    ):
        print(
            f" Event Info: Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()} Content: {event.content}"
        )
        print("_" * 50)
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = f"Agent escalated: {event.error_message} or No specific error messgae"
            break
    print(f" <<< Agent Response: {final_response_text}")
    return final_response_text


async def run_team_conversation(prompt):
    root_agent = get_agent_async()
    session_service = InMemorySessionService()

    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    runner_agent_team = Runner(
        agent=root_agent, app_name=APP_NAME, session_service=session_service
    )

    final_response_text = await call_agent_async(
        prompt, runner=runner_agent_team, user_id=USER_ID, session_id=SESSION_ID
    )

    return final_response_text


if __name__ == "__main__":
    try:
        asyncio.run(
            run_team_conversation("Who is interested in artificial intelligence?")
        )
    except Exception as e:
        print(f"Oops! An error occured: {e} ")
