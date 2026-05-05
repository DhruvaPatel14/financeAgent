# Finance Agent

A simple finance agent workflow that processes user queries, builds a research plan, orchestrates agents, and returns a final answer.

## Setup

1. Install Python 3.10+ if needed.
2. Open a terminal in this project folder.
3. Create and activate a virtual environment:

   Windows PowerShell:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   Windows Command Prompt:
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate.bat
   ```

4. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project root with any required API keys or configuration values. Example:

   ```.env
   OPENAI_API_KEY=your_ OPENAI_API_KEY
   PHI_API_KEY = your_PHI_API_KEY
   GROQ_API_KEY = your_GROQ_API_KEY
   ```

## Run

1. Start the application (if using FastAPI or a CLI entrypoint):

   ```powershell
   uvicorn financial_agent:app --reload
   ```

2. If the project is run directly from a Python script, use:

   ```powershell
   python financial_agent.py
   ```

3. Open the local server URL shown in the terminal, or send requests to the application as configured.

## Notes

- Update `.env` with valid credentials before running.
- If the application has a different entrypoint, adjust the command above to match the project structure.
