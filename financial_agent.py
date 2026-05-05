from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import openai
from query_filter import is_finance_query, is_Pharma_query
from doc_upload import load_and_store, retrieve_docs, is_docs_loaded

import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

print(os.getenv("OPENAI_API_KEY"))

# ── Web search agent ──────────────────────────────────────────────────────────
web_search_agent = Agent(
    name="Web Search Agent",
    role="Search the web for the information",
    model=OpenAIChat(model="gpt-4.1-mini"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True,
)

search_tool = YFinanceTools(
    stock_price=True,
    analyst_recommendations=True,
    stock_fundamentals=True,
    company_news=True,
)

# ── IT research agent ─────────────────────────────────────────────────────────
it_agent = Agent(
    name="IT Research Agent",
    role="Expert in IT services, SaaS, cloud, and tech companies",
    model=OpenAIChat(model="gpt-4.1-mini"),
    tools=[search_tool],
    instructions=[
        "Focus on IT sector companies",
        "Analyze revenue growth, margins, and trends",
        "Compare major players",
        "Use recent data and news",
    ],
    show_tool_calls=True,
    markdown=True,
)

# ── Pharma research agent ─────────────────────────────────────────────────────
pharma_agent = Agent(
    name="Pharma Research Agent",
    role="Expert in pharmaceutical industry, drug development, and healthcare trends",
    model=OpenAIChat(model="gpt-4.1-mini"),
    tools=[search_tool],
    instructions=[
        "Focus on pharmaceutical companies",
        "Analyze drug pipelines, clinical trial results, and regulatory news",
        "Compare major players in the pharma sector",
        "Use recent data and news",
    ],
    show_tool_calls=True,
    markdown=True,
)

# ── Multi-agent team ──────────────────────────────────────────────────────────
multi_ai_agent = Agent(
    team=[web_search_agent, it_agent, pharma_agent],
    instructions=["Always include sources", "Use table to display the data"],
    show_tool_calls=True,
    markdown=True,
)


# ── Optional document upload ──────────────────────────────────────────────────
upload_choice = input("Do you want to upload a financial document? (yes/no): ").strip().lower()

if upload_choice in ("yes", "y"):
    doc_path = input("Enter the full path to your PDF document: ").strip()
    try:
        pages = load_and_store(doc_path)
        print(f"Loaded {pages} page(s) from '{doc_path}' into the knowledge base.")
    except FileNotFoundError as e:
        print(f"[Error] {e}")
        print("Continuing without document context.")
    except ValueError as e:
        print(f"[Error] {e}")
        print("Continuing without document context.")
    except Exception as e:
        print(f"[Error] Unexpected error while loading document: {e}")
        print("Continuing without document context.")
else:
    print("Skipping document upload. Proceeding with web and market data only.")


# ── User query ────────────────────────────────────────────────────────────────
user_query = input("\nEnter your query: ").strip()

if not is_finance_query(user_query) and not is_Pharma_query(user_query):
    print("This system only handles financial and pharmaceutical research queries.")
    exit()

# ── Build enhanced query (with doc context only if docs were loaded) ───────────
if is_docs_loaded():
    context = retrieve_docs(user_query)
    enhanced_query = f"""
User Query:
{user_query}

Relevant Financial Documents:
{context}

Use the above documents to provide a more accurate analysis.
"""
else:
    # No document uploaded — send raw query directly
    enhanced_query = user_query

multi_ai_agent.print_response(enhanced_query, stream=True)