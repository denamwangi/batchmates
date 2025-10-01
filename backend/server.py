"""
FastAPI application for the BatchMates API.

This service exposes endpoints to:
- Check service health
- Retrieve batchmate profiles from a local JSON file
- Query a conversational agent for a person's interests
- Query a conversational agent for people matching an interest

CORS origins are configured via settings in `backend.core.config`.
"""
from fastapi import FastAPI, HTTPException, Query, Path, Depends
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
from backend.models.orm import Person, Interest, PersonInterest, InterestType
from backend.database import get_db
from sqlalchemy.orm import Session

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
    limit: int = Query(default=50, ge=1, le=100, description="Maximum number of profiles to return"),
    db: Session = Depends(get_db)
):
    """Get all batchmate profiles.

    Queries the database for all people and their associated interests,
    organizing them by interest type (technical, goals, hobbies, other).

    Raises:
        HTTPException 500: If database query fails.
    """
    try:
        # Query all people with their interests
        people = db.query(Person).limit(limit).all()
        
        profiles = []
        for person in people:
            # Get all interests for this person, organized by type
            person_interests = db.query(PersonInterest, Interest, InterestType).join(
                Interest, PersonInterest.interest_id == Interest.id
            ).join(
                InterestType, PersonInterest.interesttype_id == InterestType.id
            ).filter(
                PersonInterest.person_id == person.id
            ).all()
            
            # Organize interests by type
            technical_skills = []
            goals = []
            hobbies = []
            other = []
            
            for person_interest, interest, interest_type in person_interests:
                interest_name = interest.description
                type_name = interest_type.name.lower()
                
                if 'technical' in type_name:
                    technical_skills.append(interest_name)
                elif 'goal' in type_name:
                    goals.append(interest_name)
                elif 'hobby' in type_name or 'non_technical' in type_name:
                    hobbies.append(interest_name)
                else:
                    other.append(interest_name)
            
            # Create profile model
            profile_data = {
                'name': person.name or "Unknown",
                'role_and_institution': person.role_and_institution,
                'location': person.location,
                'technical_skills_and_interests': technical_skills,
                'goals': goals,
                'non_technical_hobbies_and_interest': hobbies,
                'other': other
            }
            
            profiles.append(ProfileModel(**profile_data))

        return ProfileResponse(data=profiles)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading profiles from database: {str(e)}")


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