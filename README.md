# 🌍 A2A Protocol Demo - AI-Powered Travel Planner

## What is This Project?

This is a **demonstration of the Agent-to-Agent (A2A) Protocol** using Google's ADK (Agent Development Kit). It's an AI-powered travel planning application that shows how multiple AI agents can work together to solve complex problems.

Think of it like having a team of travel experts, where each expert specializes in one area:
- 🛫 **Flight Agent**: Finds the best flight options with prices and durations
- 🏨 **Stay Agent**: Recommends accommodations with detailed pricing
- 🎯 **Activities Agent**: Suggests tourist attractions and cultural activities
- 🎭 **Host Agent**: Coordinates everything and presents the final plan

## 🏗️ How It Works (Architecture)

### The Big Picture
```
User Input (Streamlit UI)
    ↓
Host Agent (Orchestrator)
    ↓
┌─────────────┬─────────────┬─────────────┐
│ Flight      │ Stay        │ Activities  │
│ Agent       │ Agent       │ Agent       │
│ (Port 8001) │ (Port 8002) │ (Port 8003) │
└─────────────┴─────────────┴─────────────┘
    ↓
Combined Results → User
```

### What Happens Step by Step

1. **User Input**: You enter your travel details in a beautiful web interface
2. **Host Agent**: Receives your request and breaks it down into tasks
3. **Specialized Agents**: Each agent works on their specialty:
   - Flight agent finds flights within your budget
   - Stay agent finds hotels/accommodations
   - Activities agent suggests local attractions and activities
4. **Results**: All information is combined and presented back to you

### Technical Architecture

- **Frontend**: Streamlit web application (`app/travel_ui.py`)
- **Backend**: FastAPI microservices for each agent
- **AI Models**: OpenAI GPT-4o via LiteLLM
- **Communication**: HTTP REST APIs between agents
- **Session Management**: In-memory session storage
- **Data Validation**: Pydantic schemas
- **Package Management**: UV for fast Python package management

## 🛠️ Prerequisites

- **Python 3.12.10+** (managed by UV)
- **UV Package Manager** - [Install UV](https://docs.astral.sh/uv/getting-started/installation/)
- **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/edgardcham/a2a-protocol-demo.git
cd a2a-protocol-demo
```

### 2. Configure Environment
Create a `.env` file in the `app/` directory:
```bash
# app/.env
OPENAI_API_KEY=your_api_key_here
```

### 3. Install Dependencies
```bash
uv sync
```

## 🎮 Running the Application

Start **5 services** in separate terminal windows:

### Terminal 1: Flight Agent (Port 8001)
```bash
cd app && uv run python -m agents.flight_agent
```

### Terminal 2: Stay Agent (Port 8002)
```bash
cd app && uv run python -m agents.stay_agent
```

### Terminal 3: Activities Agent (Port 8003)
```bash
cd app && uv run python -m agents.activities_agent
```

### Terminal 4: Host Agent (Port 8000)
```bash
cd app && uv run python -m agents.host_agent
```

### Terminal 5: Streamlit UI (Port 8501)
```bash
uv run streamlit run app/travel_ui.py
```

## 🎯 Using the Application

1. **Open** `http://localhost:8501` in your browser
2. **Fill in the travel form**:
   - **Origin**: Where you're flying from (e.g., "New York")
   - **Destination**: Where you want to go (e.g., "Paris")
   - **Start Date**: When your trip begins
   - **End Date**: When your trip ends
   - **Budget**: How much you want to spend (in USD)
3. **Click "Plan My Trip ✨"**
4. **Review your results**:
   - ✈️ Flight options with prices and durations
   - 🏨 Accommodation recommendations with pricing
   - 🗺️ Activity suggestions with costs and time requirements

## 📁 Project Structure

```
a2a-protocol-demo/
├── app/                          # Main application code
│   ├── agents/                   # AI agent implementations
│   │   ├── host_agent/          # Main orchestrator (Port 8000)
│   │   │   ├── agent.py         # ADK agent configuration
│   │   │   ├── task_manager.py  # Coordinates other agents
│   │   │   ├── __main__.py      # Service startup script
│   │   │   └── .well-known/     # Agent discovery metadata
│   │   ├── flight_agent/        # Flight specialist (Port 8001)
│   │   ├── stay_agent/          # Accommodation specialist (Port 8002)
│   │   └── activities_agent/    # Activities specialist (Port 8003)
│   ├── common/                  # Shared utilities
│   │   ├── a2a_server.py       # FastAPI server template
│   │   └── a2a_client.py       # HTTP client for agent communication
│   ├── shared/                  # Shared data models
│   │   └── schemas.py          # Pydantic data validation schemas
│   ├── travel_ui.py            # Streamlit web interface
│   └── .env                    # Environment variables (create this)
├── .github/workflows/           # CI/CD automation
├── pyproject.toml              # Project configuration
├── uv.lock                     # Locked dependency versions
└── README.md                   # This file
```

## 📦 Dependencies

### Core Dependencies
- **fastapi** (>=0.115.12) - Modern web framework for building APIs
- **streamlit** (>=1.45.1) - Web app framework for the UI
- **google-adk** (>=1.0.0) - Agent Development Kit for AI agents
- **litellm** (>=1.71.1) - Universal interface for AI models
- **openai** (>=1.82.0) - OpenAI API client
- **pydantic** (>=2.11.5) - Data validation and serialization
- **httpx** (>=0.28.1) - Modern HTTP client for agent communication
- **python-dotenv** (>=1.1.0) - Environment variable management
- **uvicorn** (>=0.34.2) - ASGI server for FastAPI

### Development Dependencies
- **poethepoet** (>=0.34.0) - Task runner
- **pyright** (>=1.1.401) - Type checking
- **ruff** (>=0.11.11) - Fast Python linter and formatter

## 🔧 Development Commands

```bash
# Format code automatically
uv run poe format

# Check for code issues
uv run poe lint

# Type checking
uv run poe typecheck

# Run all checks
uv run poe check
```

## 🧪 Testing the API

Test individual agents directly:

```bash
# Test Flight Agent
curl -X POST http://localhost:8001/run \
  -H "Content-Type: application/json" \
  -d '{"destination": "Paris", "start_date": "2024-06-01", "end_date": "2024-06-07", "budget": 2000}'

# Test Stay Agent
curl -X POST http://localhost:8002/run \
  -H "Content-Type: application/json" \
  -d '{"destination": "Paris", "start_date": "2024-06-01", "end_date": "2024-06-07", "budget": 2000}'

# Test Activities Agent
curl -X POST http://localhost:8003/run \
  -H "Content-Type: application/json" \
  -d '{"destination": "Paris", "start_date": "2024-06-01", "end_date": "2024-06-07", "budget": 2000}'

# Test Full System (Host Agent)
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{"destination": "Paris", "start_date": "2024-06-01", "end_date": "2024-06-07", "budget": 2000}'
```

## 🐛 Troubleshooting

### Common Issues

**Services not starting?**
- Ensure you're in the correct directory (`app/` for agents)
- Check that ports 8000-8003 and 8501 are available
- Verify your OpenAI API key is set in `app/.env`

**"No stays returned" or missing data?**
- Ensure all 4 agent services are running
- Check terminal logs for error messages
- Verify agents are accessible: `curl http://localhost:800X/docs`

**Duration showing "N/A"?**
- Restart all agent services to apply schema updates
- Agents now return standardized `duration_hours` field

### Checking Service Status
```bash
# Check if all services are running
curl -s http://localhost:8001/docs > /dev/null && echo "Flight agent: ✅" || echo "Flight agent: ❌"
curl -s http://localhost:8002/docs > /dev/null && echo "Stay agent: ✅" || echo "Stay agent: ❌"
curl -s http://localhost:8003/docs > /dev/null && echo "Activities agent: ✅" || echo "Activities agent: ❌"
curl -s http://localhost:8000/docs > /dev/null && echo "Host agent: ✅" || echo "Host agent: ❌"
```

## 🎓 Learning Opportunities

This project demonstrates:

1. **Microservices Architecture** - Each agent runs as an independent service
2. **AI Agent Orchestration** - How multiple AI agents collaborate
3. **RESTful APIs** - Service-to-service communication
4. **Modern Python Development** - FastAPI, Pydantic, Streamlit, UV
5. **Prompt Engineering** - Structured JSON responses from LLMs
6. **Session Management** - Handling stateful AI conversations

## 🚀 Extending the Project

Ideas for enhancement:

1. **Add More Agents** - Weather, restaurants, transportation, currency exchange
2. **Improve UI** - Add maps, images, booking links, itinerary export
3. **Add Persistence** - Database storage for travel plans and user preferences
4. **Real API Integration** - Connect to actual booking services
5. **Authentication** - User accounts and saved trips
6. **Deployment** - Docker containers and cloud deployment

## 📝 License

This project is for educational and demonstration purposes. Check individual dependencies for their licensing terms.

---

**Happy Travels! ✈️🌍**

*Built with ❤️ using Google ADK, OpenAI, and the A2A Protocol*
