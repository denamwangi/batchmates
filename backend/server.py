from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json 
import os
from batchmates_agent.agent_runner import run_team_conversation
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

with open('./interest_mappings.json', 'r') as f:
    data = json.load(f)
    normalized_mapping = data.get('mapping')

@app.get("/")
def say_hello():
    return "Hello World"

@app.get("/profiles")
def get_profiles():
    folder_path = os.path.abspath(os.getcwd())
    INTROS_JSON_FILE_NAME = 'zulip_intros_json'
    full_path = os.path.join(folder_path, INTROS_JSON_FILE_NAME+'.json')
    with open(full_path, 'r') as f:
        intros = json.load(f)
        data = [v for _, v in intros.items()]
    return {'status': 200, 'data': data}

@app.get("/person/{person}/interests")
def get_interests(person: str):
    agent_response = asyncio.run(run_team_conversation(f"What is {person} interested in?"))
    interests = json.loads(agent_response)
    return {'status': 200, 'data': {'id': person, 'interests': interests}}

@app.get("/interest/{interest}/people")
def get_people_with_interest(interest):
    agent_response = None
    try:
        agent_response = asyncio.run(run_team_conversation(f"Who are all the people interested in {interest.lower()}?"))
    except:
        pass

    if isinstance(agent_response, str):
        people = json.loads(agent_response)
    else:
        people = agent_response

    return {'status': 200, 'data': {'id': interest, 'people': people}}