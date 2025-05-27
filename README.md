# 🌍 A2A Protocol Demo - AI-Powered Travel Planner

## What is This Project?

This is a **demonstration of the Agent-to-Agent (A2A) Protocol** using Google's ADK (Agent Development Kit). It's an AI-powered travel planning application that shows how multiple AI agents can work together to solve complex problems.

Think of it like having a team of travel experts, where each expert specializes in one area:
- 🛫 **Flight Agent**: Finds the best flight options
- 🏨 **Stay Agent**: Recommends accommodations
- 🎯 **Activities Agent**: Suggests things to do
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

## 🛠️ Prerequisites (What You Need)

Before you start, make sure you have:

1. **Python 3.12.10 or higher** - [Download here](https://python.org)
2. **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)
3. **Git** - [Download here](https://git-scm.com/)
4. **Terminal/Command Line** - Built into Mac/Linux, or use PowerShell on Windows

## 🚀 Installation & Setup

### Step 1: Clone the Repository
```bash
# Download the project to your computer
git clone https://github.com/edgardcham/a2a-protocol-demo.git
cd a2a-protocol-demo
```

### Step 2: Set Up Python Environment
```bash
# Create a virtual environment (like a sandbox for this project)
python -m venv .venv

# Activate the virtual environment
# On Mac/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
# Install all required packages
pip install -e .
```

### Step 4: Configure Environment Variables
```bash
# Create a file to store your API keys
touch .env

# Add your OpenAI API key to the .env file
echo "OPENAI_API_KEY=your_api_key_here" >> .env
```

**Important**: Replace `your_api_key_here` with your actual OpenAI API key!

## 🎮 How to Run the Application

You need to start **4 different services** in **4 separate terminal windows**. Think of each as a different worker in your travel agency.

### Terminal 1: Flight Agent
```bash
cd app/agents/flight_agent
python -m app.agents.flight_agent
```
This starts the flight booking specialist on port 8001.

### Terminal 2: Stay Agent
```bash
cd app/agents/stay_agent
python -m app.agents.stay_agent
```
This starts the accommodation specialist on port 8002.

### Terminal 3: Activities Agent
```bash
cd app/agents/activities_agent
python -m app.agents.activities_agent
```
This starts the activities specialist on port 8003.

### Terminal 4: Host Agent (Main Coordinator)
```bash
cd app/agents/host_agent
python -m app.agents.host_agent
```
This starts the main coordinator on port 8000.

### Terminal 5: Web Interface
```bash
# In the project root directory
streamlit run app/travel_ui.py
```
This opens the web interface in your browser (usually at http://localhost:8501).

## 🎯 How to Use the Application

1. **Open your browser** and go to `http://localhost:8501`
2. **Fill in the travel form**:
   - **Origin**: Where you're flying from (e.g., "New York")
   - **Destination**: Where you want to go (e.g., "Paris")
   - **Start Date**: When your trip begins
   - **End Date**: When your trip ends
   - **Budget**: How much you want to spend (in USD)
3. **Click "Plan My Trip ✨"**
4. **Wait for the magic** - The AI agents will work together to create your plan
5. **Review your results**:
   - ✈️ Flight options with prices and durations
   - 🏨 Accommodation recommendations
   - 🗺️ Activity suggestions

## 📁 Project Structure Explained

```
a2a-protocol-demo/
├── app/                          # Main application code
│   ├── agents/                   # AI agent implementations
│   │   ├── host_agent/          # Main orchestrator
│   │   │   ├── agent.py         # Agent logic and configuration
│   │   │   ├── task_manager.py  # Coordinates other agents
│   │   │   ├── __main__.py      # Service startup script
│   │   │   └── .well-known/     # Agent discovery metadata
│   │   ├── flight_agent/        # Flight booking specialist
│   │   ├── stay_agent/          # Accommodation specialist
│   │   └── activities_agent/    # Activities specialist
│   ├── common/                  # Shared utilities
│   │   ├── a2a_server.py       # FastAPI server template
│   │   └── a2a_client.py       # HTTP client for agent communication
│   ├── shared/                  # Shared data models
│   │   └── schemas.py          # Pydantic data validation schemas
│   └── travel_ui.py            # Streamlit web interface
├── .github/workflows/           # Automated testing and linting
├── pyproject.toml              # Project configuration and dependencies
├── uv.lock                     # Locked dependency versions
├── main.py                     # Simple entry point
└── README.md                   # This file!
```

## 🔧 Development Tools

This project includes several development tools to maintain code quality:

### Code Formatting and Linting
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

### Dependencies Used

- **FastAPI**: Modern web framework for building APIs
- **Streamlit**: Easy web app framework for data science
- **Google ADK**: Agent Development Kit for building AI agents
- **LiteLLM**: Universal interface for different AI models
- **OpenAI**: Access to GPT models
- **Pydantic**: Data validation and serialization
- **HTTPX**: Modern HTTP client for Python
- **python-dotenv**: Environment variable management

## 🐛 Troubleshooting

### Common Issues and Solutions

**Problem**: "ModuleNotFoundError" when running agents
**Solution**: Make sure you're in the correct directory and have activated your virtual environment

**Problem**: "Connection refused" errors
**Solution**: Make sure all 4 agent services are running in separate terminals

**Problem**: "Invalid API key" errors
**Solution**: Check that your `.env` file contains the correct OpenAI API key

**Problem**: Agents return "No results"
**Solution**: Check that all agents are running and accessible on their respective ports

**Problem**: Streamlit won't start
**Solution**: Make sure you're running the command from the project root directory

### Checking if Services are Running
```bash
# Check if services are responding
curl http://localhost:8001/docs  # Flight agent
curl http://localhost:8002/docs  # Stay agent
curl http://localhost:8003/docs  # Activities agent
curl http://localhost:8000/docs  # Host agent
```

## 🎓 Learning Opportunities

This project demonstrates several important concepts:

1. **Microservices Architecture**: Each agent runs as an independent service
2. **AI Agent Orchestration**: How multiple AI agents can work together
3. **RESTful APIs**: Communication between services using HTTP
4. **Modern Python Development**: Using tools like FastAPI, Pydantic, and Streamlit
5. **Environment Management**: Proper handling of API keys and configuration
6. **Code Quality**: Automated formatting, linting, and type checking

## 🚀 Next Steps

Want to extend this project? Here are some ideas:

1. **Add More Agents**: Create agents for restaurants, weather, or transportation
2. **Improve UI**: Add maps, images, or more interactive elements
3. **Add Persistence**: Store travel plans in a database
4. **Add Authentication**: User accounts and saved preferences
5. **Deploy to Cloud**: Make it accessible to others online
6. **Add Real APIs**: Connect to actual flight and hotel booking services

## 📝 License

This project is for educational and demonstration purposes. Please check individual dependencies for their licensing terms.

## 🤝 Contributing

This is a demo project, but feel free to fork it and make it your own! If you find bugs or have suggestions, please open an issue.

---

**Happy Travels! ✈️🌍**

*Built with ❤️ using Google ADK and the A2A Protocol*
