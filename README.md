# BatchMates

A web application that visualizes and explores connections between Recurse Center batchmates through their shared interests and skills. Built with React, Material UI, and FastAPI, it uses LLM-powered data processing to create an interactive network graph and profile cards.

## Features

- **Interactive Network Graph**: Visualize connections between people and their shared interests using react-force-graph
- **Profile Cards**: Browse individual profiles with structured information about each person
- **Interest-Based Navigation**: Click on interests to see who shares them, or click on people to see their interests
- **LLM-Powered Data Processing**: Uses OpenAI models to extract and normalize structured data from informal introductions
- **Database Integration**: PostgreSQL backend with SQLAlchemy ORM for data persistence
- **AI Agent Integration**: Google ADK agent with MCP tools for intelligent querying of the database

## Tech Stack

### Frontend
- **React 19** with React Router for navigation
- **Material UI** for component styling and layout
- **react-force-graph** for interactive network visualization

### Backend
- **FastAPI** for REST API endpoints
- **PostgreSQL** with SQLAlchemy ORM for data storage
- **OpenAI API** for LLM-powered data processing
- **Google ADK** with MCP (Model Context Protocol) for intelligent database querying
- **Zulip API** for data collection from Recurse Center introductions

### Data Processing
- **LLM Summarization**: Extracts structured data from informal introductions using `prompts/intro_summarize.txt`
- **Interest Normalization**: Groups similar interests into standardized categories using `prompts/intro_interests_normalize.txt`
- **Relationship Mapping**: Creates connections between people based on shared interests
- **Modular Prompts**: Text-based prompt templates for easy customization and version control

## System Architecture

```mermaid
graph TB
  Z[Zulip API] --> P[LLM Processing<br/>OpenAI GPT-4]
  P --> DB[(PostgreSQL)]
  P --> JSON[data/zulip_intros_json.json]

  DB --> AGENT[AI Agent with MCP]
  JSON --> API[FastAPI REST API]
  API -.-> AGENT
  
  API --> REACT[React Frontend]
  REACT --> CV[Card View]
  REACT --> GV[Graph View]

  %% Data flow arrows show progression from source to storage and interfaces
```

### Architecture Components

**🔄 Data Flow:**
1. **Collection**: Zulip API provides raw introduction messages
2. **Processing**: LLM extracts structured data using modular prompts
3. **Normalization**: Interests are categorized and standardized
4. **Storage**: Data is stored in PostgreSQL with proper relationships
5. **Visualization**: React frontend displays interactive network and profiles

**🤖 AI Integration:**
- **LLM Processing**: OpenAI GPT-4o-mini for data extraction and normalization
- **Agent System**: Google ADK with MCP tools for intelligent database querying
- **Prompt Management**: Text-based templates for easy customization
 - **REST API Integration**: FastAPI can route certain queries through the LLM agent for natural-language powered results

#### Agent Invocation and Postgres Access
The Postgres server is accessed through the agent run flow. Calls like the following execute the ADK/MCP-backed agent, which queries Postgres using `DB_URL`:

```python
agent_response = asyncio.run(run_team_conversation("Who is interested in artificial intelligence?"))
```

**🌐 User Interfaces:**
- **Web Application**: React-based UI for browsing profiles and network visualization
- **ADK Interface**: Google ADK web UI for testing and interacting with the AI agent
- **REST API**: FastAPI endpoints for frontend-backend communication

**🗄️ Data Management:**
- **Structured Storage**: PostgreSQL with SQLAlchemy ORM
- **File Organization**: Centralized `data/` directory for generated files
- **Schema Design**: Normalized database with proper relationships

## Project Structure

```
batchmates/
├── backend/                 # FastAPI backend
│   ├── server.py           # Main API server with endpoints
│   ├── db_init.py          # Database initialization and seeding operations
│   ├── process_data.py     # Data processing and LLM integration
│   └── models/             # Database models and schemas
│       ├── orm.py          # SQLAlchemy ORM models
│       └── schemas.py      # Pydantic schemas
├── batchmates_agent/       # AI agent for database querying
│   ├── agent.py            # Google ADK agent configuration
│   ├── agent_runner.py     # Agent execution and session management
│   └── constants.py        # Agent configuration constants
├── prompts/                # LLM prompt templates
│   ├── intro_summarize.txt # Prompt for extracting structured data
│   ├── intro_interests_normalize.txt # Prompt for interest normalization
│   └── rcdb_agent_instructions.txt # Agent system instructions
├── data/                   # Generated data files
│   ├── raw_introductions.csv
│   ├── zulip_intros_json.json
│   ├── interest_mappings.json
│   └── network_data.json
├── src/                    # React frontend
│   ├── App.js              # Main app component with routing
│   ├── CardView.js         # Profile cards view
│   ├── GraphView.js        # Network graph visualization
│   └── Profile.js          # Individual profile component
├── build/                  # Production build output
└── public/                 # Static assets
```

## API Endpoints

- `GET /` - Health check endpoint
- `GET /profiles` - Retrieve all batchmate profiles
- `GET /person/{person}/interests` - Get interests for a specific person
- `GET /interest/{interest}/people` - Get people interested in a specific topic

## Data Model

The application uses a normalized database schema with the following key entities:

- **People**: Basic profile information (name, location, role)
- **Interests**: Individual interests and skills
- **Normalized Interests**: Standardized categories for grouping similar interests
- **Interest Types**: Categories like "technical_skills_and_interests", "non_technical_hobbies_and_interest"
- **Person Interests**: Many-to-many relationships linking people to their interests

## Setup and Installation

### Prerequisites
- Python 3.10+
- Node.js 18+
- PostgreSQL database
- OpenAI API key
- Zulip API credentials (for data collection)

### Backend Setup
1. Create a virtual environment:
   ```bash
   python -m venv venv-py310
   source venv-py310/bin/activate  # On Windows: venv-py310\Scripts\activate
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export ZULIP_SECRET="your_zulip_api_key"
   export DB_URL="postgresql://username:password@localhost:5432/rcdb"
   export OPENAI_API_KEY="your_openai_api_key"  # For LLM processing
   ```

4. Initialize the database:
   ```bash
   python -m backend.db_init
   ```

5. Start the FastAPI server:
   ```bash
   uvicorn backend.server:app --reload --port 8080
   ```

6. Launch the Google ADK UI (optional):
   ```bash
   adk web
   ```
   This opens the Google ADK web interface for testing and interacting with the AI agent.

### Frontend Setup
1. Install Node.js dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```

The application will be available at `http://localhost:3000` with the API running on `http://localhost:8080`.

## Usage

1. **Browse Profiles**: Visit the home page to see all batchmate profiles in card format
2. **Explore Graph**: Navigate to `/graph` to see the interactive network visualization
3. **Discover Connections**: Click on any interest to see who shares it, or click on a person to see their interests
4. **Deep Dive**: Use the AI agent to ask natural language questions about the data
5. **Test AI Agent**: Run `adk web` to open the Google ADK UI for testing agent interactions

## Data Sources

The application processes data from:
- Recurse Center Zulip introductions
- LLM-extracted structured information
- Normalized interest categories
- Relationship mappings between people and interests

## Data Management

The application organizes all generated data in the `data/` directory:

- **Raw Data**: `raw_introductions.csv` - Original Zulip messages
- **Structured Data**: `zulip_intros_json.json` - LLM-extracted profiles
- **Normalized Data**: `interest_mappings.json` - Standardized interest categories
- **Network Data**: `network_data.json` - Graph relationships for visualization

All data files are automatically created and managed by the processing pipeline. The `data/` directory is created automatically if it doesn't exist.

### Prompt Customization

LLM prompts are stored as text files in the `prompts/` directory for easy editing:

- `intro_summarize.txt` - Controls how introductions are structured
- `intro_interests_normalize.txt` - Controls interest categorization logic
- `rcdb_agent_instructions.txt` - Agent behavior and database query instructions

Modify these files to adjust the LLM behavior without changing code.

## Development

The project includes:
- **Modular Architecture**: Separated concerns with dedicated directories for prompts, data, and models
- **Text-Based Prompts**: Easy-to-edit prompt templates for LLM customization
- **Organized Data Management**: Centralized data directory with clear file purposes
- **Comprehensive Data Processing Pipeline**: From raw Zulip data to interactive visualizations
- **AI Agent Integration**: Google ADK with MCP tools for intelligent database querying
- **RESTful API Design**: Clean endpoints for frontend integration
- **Modern React Patterns**: Hooks, routing, and component-based architecture
- **Database-First Approach**: SQLAlchemy ORM with proper schema management

## Contributing

This project is designed for the Recurse Center community to better understand and connect with fellow batchmates through shared interests and skills.