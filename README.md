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
- **LLM Summarization**: Extracts structured data from informal introductions
- **Interest Normalization**: Groups similar interests into standardized categories
- **Relationship Mapping**: Creates connections between people based on shared interests

## Project Structure

```
batchmates/
├── backend/                 # FastAPI backend
│   ├── server.py           # Main API server with endpoints
│   ├── data.py             # SQLAlchemy models and database operations
│   ├── process_data.py     # Data processing and LLM integration
│   └── prompt.py           # LLM prompts for data extraction
├── batchmates_agent/       # AI agent for database querying
│   ├── agent.py            # Google ADK agent configuration
│   ├── agent_runner.py     # Agent execution and session management
│   └── constants.py        # Agent configuration constants
├── src/                    # React frontend
│   ├── App.js              # Main app component with routing
│   ├── CardView.js         # Profile cards view
│   ├── GraphView.js        # Network graph visualization
│   └── Profile.js          # Individual profile component
├── build/                  # Production build output
├── public/                 # Static assets
└── data files/             # JSON and CSV data files
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
   ```

4. Initialize the database:
   ```bash
   python backend/data.py
   ```

5. Start the FastAPI server:
   ```bash
   uvicorn backend.server:app --reload --port 8080
   ```

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

## Data Sources

The application processes data from:
- Recurse Center Zulip introductions
- LLM-extracted structured information
- Normalized interest categories
- Relationship mappings between people and interests

## Development

The project includes:
- Comprehensive data processing pipeline
- LLM integration for data extraction and normalization
- Interactive visualization components
- AI agent for intelligent database querying
- RESTful API design
- Modern React patterns with hooks and routing

## Contributing

This project is designed for the Recurse Center community to better understand and connect with fellow batchmates through shared interests and skills.