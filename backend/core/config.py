"""
Configuration management for the BatchMates application.
Simple environment variable handling with sensible defaults.
"""
import os
from typing import List


# External API Keys
ZULIP_SECRET = os.environ.get("ZULIP_SECRET")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Database Configuration
DATABASE_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql://denamwangi:mcppassword@localhost:5432/rcdb"
)

# API Configuration
API_HOST = os.environ.get("API_HOST", "127.0.0.1")
API_PORT = int(os.environ.get("API_PORT", "8080"))
API_TITLE = os.environ.get("API_TITLE", "BatchMates API")
API_VERSION = os.environ.get("API_VERSION", "1.0.0")

# CORS Configuration
CORS_ORIGINS = os.environ.get(
    "CORS_ORIGINS", 
    "http://localhost:3000,http://127.0.0.1:3000"
).split(",")


# File Paths
DATA_DIR = "./"
INTEREST_MAPPINGS_FILE = "interest_mappings.json"
PROFILES_FILE = "zulip_intros_json.json"

# AI Agent Configuration
AGENT_MODEL = "openai/gpt-4o-mini"
AGENT_APP_NAME = "rc_batchmates_app"
AGENT_USER_ID = "test_user_1"
AGENT_SESSION_ID = "session_001"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def get_database_url() -> str:
    """Get the database URL."""
    return DATABASE_URL


def get_file_path(filename: str) -> str:
    """Get the full path for a data file."""
    return os.path.join(DATA_DIR, filename)


def get_cors_origins() -> List[str]:
    """Get CORS origins as a list."""
    return CORS_ORIGINS
