"""
Pydantic models for request/response validation and serialization.
Provides type safety and automatic validation for API endpoints.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator


class BaseResponse(BaseModel):
    """Base response model with common fields."""
    status: int = Field(default=200, description="HTTP status code")
    message: Optional[str] = Field(default=None, description="Response message")


class ErrorResponse(BaseResponse):
    """Error response model."""
    status: int = Field(default=400, description="HTTP status code")
    error_code: str = Field(description="Application-specific error code")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Additional error details")


class ProfileModel(BaseModel):
    """Profile data model."""
    name: str = Field(description="Person's name")
    role_and_institution: Optional[str] = Field(default=None, description="Current role and institution")
    location: Optional[str] = Field(default=None, description="Location")
    technical_skills_and_interests: List[str] = Field(default_factory=list, description="Technical skills and interests")
    goals: List[str] = Field(default_factory=list, description="Goals at Recurse Center")
    non_technical_hobbies_and_interest: List[str] = Field(default_factory=list, description="Non-technical hobbies and interests")
    other: List[str] = Field(default_factory=list, description="Other information")
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip()


class ProfileResponse(BaseResponse):
    """Response model for profile data."""
    data: List[ProfileModel] = Field(description="List of profiles")


class PersonInterestsResponse(BaseResponse):
    """Response model for a person's interests."""
    data: Dict[str, Any] = Field(description="Person and their interests")
    
    class Config:
        schema_extra = {
            "example": {
                "status": 200,
                "data": {
                    "id": "John Doe",
                    "interests": ["rust", "machine learning", "cooking"]
                }
            }
        }


class InterestPeopleResponse(BaseResponse):
    """Response model for people interested in a specific topic."""
    data: Dict[str, Any] = Field(description="Interest and people who share it")
    
    class Config:
        schema_extra = {
            "example": {
                "status": 200,
                "data": {
                    "id": "rust",
                    "people": ["Alice", "Bob", "Charlie"]
                }
            }
        }


class InterestModel(BaseModel):
    """Interest data model."""
    name: str = Field(description="Interest name")
    normalized_name: Optional[str] = Field(default=None, description="Normalized interest name")
    type: Optional[str] = Field(default=None, description="Type of interest (technical, non-technical, etc.)")
    people_count: Optional[int] = Field(default=None, description="Number of people with this interest")


class InterestListResponse(BaseResponse):
    """Response model for a list of interests."""
    data: List[InterestModel] = Field(description="List of interests")


class HealthCheckResponse(BaseModel):
    """Health check response model."""
    status: str = Field(description="Service status")
    version: str = Field(description="API version")
    timestamp: str = Field(description="Response timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": "2024-01-01T00:00:00Z"
            }
        }


# Request models for future use
class ProfileSearchRequest(BaseModel):
    """Request model for searching profiles."""
    query: str = Field(description="Search query")
    limit: Optional[int] = Field(default=10, ge=1, le=100, description="Maximum number of results")
    include_interests: bool = Field(default=True, description="Include interests in results")


class InterestSearchRequest(BaseModel):
    """Request model for searching interests."""
    query: str = Field(description="Search query")
    limit: Optional[int] = Field(default=20, ge=1, le=100, description="Maximum number of results")
    interest_type: Optional[str] = Field(default=None, description="Filter by interest type")


# Simple models for toy project - removed complex validation


# Validation helpers
def validate_person_name(name: str) -> str:
    """Validate and normalize person name."""
    if not name or not name.strip():
        raise ValueError("Person name cannot be empty")
    return name.strip()


def validate_interest_name(interest: str) -> str:
    """Validate and normalize interest name."""
    if not interest or not interest.strip():
        raise ValueError("Interest name cannot be empty")
    return interest.strip().lower()
