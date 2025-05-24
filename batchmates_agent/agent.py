from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
import os

load_dotenv()

postgres_url = os.getenv('DB_URL')
if not postgres_url:
    raise ValueError("Add DB_URL to .env file")

MODEL_GPT_40='openai/gpt-4o-mini'
def get_prompt():
    with open('./rcdb_agent_instructions.txt', 'r') as f:
        prompt = f.read()
        print(prompt)
        return prompt

"""Creates an ADK Agent equipped with tools from the MCP Server."""
rcdb_tools = MCPToolset(
            connection_params=StdioServerParameters(
                command='npx',
                args=[
                    "-y", 
                "@modelcontextprotocol/server-postgres",
                f"{postgres_url}"
            ],
            ),
        )
root_agent = LlmAgent(
    model=LiteLlm(MODEL_GPT_40),
    name='recurse_center_info_agent',
    instruction=get_prompt(),
    tools=[rcdb_tools]
)
