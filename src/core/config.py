import os
from dotenv import load_dotenv

load_dotenv()

EXCHANGERATE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")

# Set LangSmith environment variables
os.environ["LANGSMITH_API_KEY"] = LANGSMITH_API_KEY
os.environ["LANGSMITH_TRACING"] = LANGSMITH_TRACING
os.environ["LANGSMITH_PROJECT"] = LANGSMITH_PROJECT
