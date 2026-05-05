from phi.agent import Agent
from phi.model.openai import OpenAIChat


def is_finance_query(query: str) -> bool:
    keywords = [
        "financial", "revenue", "profit", "market", "stock", "analysis", "stocks","Large-cap", "mid-cap", "small-cap",
        "Loss", "gain", "investment", "company", "sector", "growth","contracts","analyze","trends","performance","valuation","earnings","guidance","dividends","cash flow","balance sheet",
        "documents","reports","filings","10-K","10-Q","earnings call","investor presentation"
    ]
    return any(k in query.lower() for k in keywords)

def is_Pharma_query(query: str) -> bool:
    keywords = [
       "pharma", "pharmaceutical", "drug", "clinical trial", "regulatory", "healthcare", "biotech",
       "vaccine", "FDA", "pipeline", "research", "development", "approval", "pharma companies",
       "pharmaceutical companies", "pharmaceutical industry", "drug development", "clinical trial results",
         "regulatory news", "pharma sector", "biotechnology", "biotech companies", "biotech industry"
    ]
    return any(k in query.lower() for k in keywords)