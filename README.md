# AI Agent with MCPs using Gemini and PydanticAI

A Python-based AI agent that uses Google Gemini as the LLM and PydanticAI as the agent framework. It integrates with MCP (Model Context Protocol) servers to extend its capabilities, including real-time time lookups and Airbnb listing searches.

## Features

- Basic Q&A powered by Gemini
- Custom date/time tool using Python's datetime
- MCP Time Server integration for timezone-aware time queries
- Airbnb search and listing details via the OpenBnB MCP server

## Prerequisites

- Python 3.10 or higher
- Node.js and npx (required for the Airbnb MCP server)
- A Google API key with access to the Gemini API

## Setup

1. Clone or navigate to the project directory.

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your API key:

```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

Run the test script:

```bash
python test_agent.py
```

You will see a menu with the following options:

| Option | Description                              |
|--------|------------------------------------------|
| 1      | Basic agent test (general Q&A)           |
| 2      | Custom date tool test                    |
| 3      | MCP Time Server test                     |
| 4      | Airbnb agent test (needs Node.js/npx)    |
| 5      | Run all tests                            |
| 0      | Exit                                     |

Enter one or more choices separated by commas (e.g. `1,3`).

## Google Colab

The `build_airbnb_agent_mcp.ipynb` notebook contains a Colab-ready version of the Airbnb agent. Open it in Google Colab, add your API key via Colab Secrets, and run the cells.

## Project Structure

```
.
├── .env                          # Environment variables (API key)
├── build_airbnb_agent_mcp.ipynb  # Colab notebook for the Airbnb agent
├── requirements.txt              # Python dependencies
├── test_agent.py                 # Local test script with interactive menu
└── venv/                         # Python virtual environment
```
