from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json 
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

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
        data = [v for k, v in intros.items()]
        print('****', data)
    return {'status': 200, 'data': data}

@app.get("/person/{person}/interests")
def get_interests(person: str):
    print(f"\n getting interest for {person} \n")
    folder_path = os.path.abspath(os.getcwd())
    INTROS_JSON_FILE_NAME = 'zulip_intros_json'
    full_path = os.path.join(folder_path, INTROS_JSON_FILE_NAME+'.json')
    with open(full_path, 'r') as f:
        intros = json.load(f)
        interests = next((v.get('technical_skills_and_interests') for k, v in intros.items() if k.lower() == person.lower()), [])
        print('****', interests)
    return {'status': 200, 'data': {'id': person, 'interests': interests}}

@app.get("/interest/{interest}/people")
def get_people_with_interest():
    folder_path = os.path.abspath(os.getcwd())
    INTROS_JSON_FILE_NAME = 'zulip_intros_json'
    full_path = os.path.join(folder_path, INTROS_JSON_FILE_NAME+'.json')
    with open(full_path, 'r') as f:
        intros = json.load(f)
        data = [v for k, v in intros.items()]
        print('****', data)
    return {'status': 200, 'data': data}