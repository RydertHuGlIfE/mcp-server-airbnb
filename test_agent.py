"""
AI Agent with MCPs using Gemini and PydanticAI
-----------------------------------------------
Local test script — run this in VSCode to verify before deploying to Colab.

Usage:
  1. Create a .env file with: GOOGLE_API_KEY=your_key_here     
  2. pip install -r requirements.txt
  3. python test_agent.py
  4: You guys dont need any genai module as pydantic handles that
"""

import os
import asyncio
from dotenv import load_dotenv

# ── Step 1: Load environment ──────────────────────────────────────────────────
load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError(" GOOGLE_API_KEY not found. Add it to your .env file.")
print("API key loaded from .env")


# ── Step 2: Create Gemini model ───────────────────────────────────────────────
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

provider = GoogleProvider(api_key=api_key)
agent_model = GoogleModel("gemini-2.5-flash", provider=provider)
print("Gemini model initialized.")


# ── Step 3: Create a basic agent ──────────────────────────────────────────────
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

agent = Agent(model=agent_model)


async def run_async(prompt: str) -> str:
    async with agent.run_mcp_servers():
        result = await agent.run(prompt)
        return result.output


async def test_basic():
    print("\n── Test: Basic Agent ──")
    response = await run_async("What is the capital of France?")
    print(f"Response: {response}")


# ── Step 4: Agent with custom date/time tool ──────────────────────────────────
from datetime import datetime
from pydantic_ai import Tool


@Tool
def get_current_date() -> str:
    """Return the current date/time as an ISO-formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


async def test_custom_tool():
    global agent
    agent = Agent(
        model=agent_model,
        tools=[get_current_date],
        system_prompt=(
            "You have access to:\n"
            "   1. get_current_date()\n"
            "Use this tool for date/time questions."
        ),
    )
    print("\n── Test: Custom Date Tool ──")
    response = await run_async("What's the date today?")
    print(f"Response: {response}")


# ── Step 5: Agent with MCP time server ────────────────────────────────────────
async def test_mcp_time():
    global agent
    time_server = MCPServerStdio(
        "python",
        args=["-m", "mcp_server_time", "--local-timezone=Asia/Kolkata"],
    )

    agent = Agent(
        model=agent_model,
        toolsets=[time_server],
        system_prompt=(
            "You are a helpful agent and you have access to this tool:\n"
            "   get_current_time(params: dict)\n"
            "When the user asks for the current date or time, call get_current_time.\n"
        ),
    )
    print("\n── Test: MCP Time Server ──")
    response = await run_async("What's the date today?")
    print(f"Response: {response}")


# ── Step 6: Airbnb agent (requires Node.js / npx) ────────────────────────────
async def test_airbnb():
    global agent
    time_server = MCPServerStdio(
        "python",
        args=["-m", "mcp_server_time", "--local-timezone=Asia/Kolkata"],
        timeout=60,
    )
    airbnb_server = MCPServerStdio(
        "npx",
        args=["-y", "@openbnb/mcp-server-airbnb", "--ignore-robots-txt"],
        timeout=60,
    )

    system_prompt = """
You have access to three tools:
1. get_current_time(params: dict)
2. airbnb_search(params: dict)
3. airbnb_listing_details(params: dict)
When the user asks for listings, first call get_current_time, then airbnb_search, etc.
"""

    agent = Agent(
        model=agent_model,
        toolsets=[time_server, airbnb_server],
        system_prompt=system_prompt,
    )
    print("\n── Test: Airbnb Agent ──")
    response = await run_async(
        "Find a place to stay in Vancouver for next Sunday for 3 nights for 2 adults?"
    )
    print(f"Response: {response}")


# ── Main ──────────────────────────────────────────────────────────────────────
MENU = """
╔══════════════════════════════════════════════╗
║   Gemini + PydanticAI + MCP — Local Test     ║
╠══════════════════════════════════════════════╣
║  1. Basic Agent Test                         ║
║  2. Custom Date Tool Test                    ║
║  3. MCP Time Server Test                     ║
║  4. Airbnb Agent Test (needs Node.js/npx)    ║
║  5. Run ALL Tests                            ║
║  0. Exit                                     ║
╚══════════════════════════════════════════════╝
"""

TEST_MAP = {
    1: ("Basic Agent", "test_basic"),
    2: ("Custom Date Tool", "test_custom_tool"),
    3: ("MCP Time Server", "test_mcp_time"),
    4: ("Airbnb Agent", "test_airbnb"),
}


async def main():
    print(MENU)
    raw = input("Enter your choice(s) (comma-separated, e.g. 1,3): ").strip()

    if not raw:
        print(" No choice entered. Exiting.")
        return

    # Parse & validate
    try:
        choices = [int(c.strip()) for c in raw.split(",")]
    except ValueError:
        print(" Invalid input. Please enter numbers separated by commas.")
        return

    if 0 in choices:
        print("Bye!")
        return

    # '5' means run all
    if 5 in choices:
        choices = [1, 2, 3, 4]

    valid = {0, 1, 2, 3, 4, 5}
    invalid = [c for c in choices if c not in valid]
    if invalid:
        print(f"❌ Invalid choice(s): {invalid}. Pick from 0-5.")
        return

    # Dispatch
    test_funcs = {
        1: test_basic,
        2: test_custom_tool,
        3: test_mcp_time,
        4: test_airbnb,
    }

    for ch in choices:
        name, _ = TEST_MAP[ch]
        print(f"\n Running: {name}")
        await test_funcs[ch]()

    print("\n Selected tests passed!")


if __name__ == "__main__":
    asyncio.run(main())
