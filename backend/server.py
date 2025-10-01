"""
FastAPI application for the BatchMates API.

This service exposes endpoints to:
- Check service health
- Retrieve batchmate profiles from a local JSON file
- Query a conversational agent for a person's interests
- Query a conversational agent for people matching an interest

CORS origins are configured via settings in `backend.core.config`.
"""
from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.middleware.cors import CORSMiddleware
import json 
import os
from batchmates_agent.agent_runner import run_team_conversation
import asyncio
from backend.core.config import get_cors_origins
from backend.models.schemas import (
    ProfileResponse, ProfileModel, PersonInterestsResponse, InterestPeopleResponse,
    HealthCheckResponse
)

app = FastAPI(
    title="BatchMates API",
    description="API for exploring connections between Recurse Center batchmates",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    allow_credentials=True
)


# Simple error handling - just let FastAPI handle it with HTTPException

with open('./data/interest_mappings.json', 'r') as f:
    data = json.load(f)
    normalized_mapping = data.get('mapping')

@app.get("/", response_model=HealthCheckResponse)
def health_check():
    """Health check endpoint.

    Returns a static payload indicating service health, API version, and a
    placeholder timestamp. In production, replace the timestamp with the
    current time.
    """
    return HealthCheckResponse(
        status="healthy",
        version="1.0.0",
        timestamp="2024-01-01T00:00:00Z"  # In production, use actual timestamp
    )


@app.get("/profiles", response_model=ProfileResponse)
def get_profiles(
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of profiles to return")
):
    """Get all batchmate profiles.

    Reads profiles from `zulip_intros_json.json` in the current working
    directory, coerces each record into a `ProfileModel`, and returns up to
    `limit` items.

    Raises:
        HTTPException 404: If the profiles file is not found.
        HTTPException 500: If the JSON is invalid or coercion fails.
    """
    try:
        folder_path = os.path.abspath(os.getcwd())
        full_path = os.path.join(folder_path, 'data', 'zulip_intros_json.json')
        print('full_path', full_path)
        with open(full_path, 'r') as f:
            intros = json.load(f)

        profiles = []
        for key, v in intros.items():
            raw_name = v.get('name') or ""
            safe_name = raw_name.strip()
            if not safe_name:
                safe_name = (key or "").strip() or "Unknown"
            payload = {
                'name': safe_name,
                'role_and_institution': v.get('role_and_institution'),
                'location': v.get('location'),
                'technical_skills_and_interests': v.get('technical_skills_and_interests') or [],
                'goals': v.get('goals') or [],
                'non_technical_hobbies_and_interest': v.get('non_technical_hobbies_and_interest') or [],
                'other': v.get('other') or []
            }
            profiles.append(ProfileModel(**payload))

        # Apply limit
        if limit < len(profiles):
            profiles = profiles[:limit]

        return ProfileResponse(data=profiles)
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Profiles file not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON in profiles file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading profiles: {str(e)}")


@app.get("/person/{person}/interests", response_model=PersonInterestsResponse)
def get_person_interests(
    person: str = Path(..., min_length=1, max_length=100, description="Person's name")
):
    """Get interests for a specific person.

    Uses the agent runner to query interests for `person`. The agent response
    is expected to be a JSON array of strings.

    Raises:
        HTTPException 500: On agent errors or invalid response format.
    """
    try:
        agent_response = asyncio.run(run_team_conversation(f"What is {person} interested in?"))
        
        if not agent_response:
            raise HTTPException(status_code=500, detail="No response from agent service")
            
        interests = json.loads(agent_response)
        
        if not isinstance(interests, list):
            raise HTTPException(status_code=500, detail="Invalid response format from agent")
            
        return PersonInterestsResponse(
            data={'id': person, 'interests': interests}
        )
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from agent")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting interests for {person}: {str(e)}")


@app.get("/interest/{interest}/people", response_model=InterestPeopleResponse)
def get_people_with_interest(
    interest: str = Path(..., min_length=1, max_length=100, description="Interest name")
):
    """Get people interested in a specific topic.

    Uses the agent runner to find people who share the specified `interest`.
    The agent response is expected to be a JSON array of strings (names).

    Raises:
        HTTPException 500: On agent errors or invalid response format.
    """
    try:
        agent_response = asyncio.run(run_team_conversation(f"Who are all the people interested in {interest.lower()}?"))
        
        if not agent_response:
            raise HTTPException(status_code=500, detail="No response from agent service")
        
        if isinstance(agent_response, str):
            people = json.loads(agent_response)
        else:
            people = agent_response
            
        if not isinstance(people, list):
            raise HTTPException(status_code=500, detail="Invalid response format from agent")
            
        return InterestPeopleResponse(
            data={'id': interest, 'people': people}
        )
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON response from agent")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting people for interest {interest}: {str(e)}")