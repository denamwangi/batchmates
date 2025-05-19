from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json 

INTROS_JSON_FILE_NAME = '../zulip_intros_json.json'
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
    with open(INTROS_JSON_FILE_NAME, 'r') as f:
        intros = json.load(f)
        data = [v for k, v in intros.items()]
    return {'status': 200, 'data': data}