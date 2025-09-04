import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
    ANTHROPIC_API_KEY =os.getenv("ANTHROPIC_API_KEY")
    FAISS_FOLDER_1="faiss_2.6-Shivaji_Nagar_Assembly-index"
    FAISS_FOLDER_2="faiss_2.7-Shivaji_Nagar_Assembly-index"
    EMBEDDING_MODEL="text-embedding-3-large"
    # LLM_MODEL="gpt-4o-mini"
    LLM_MODEL="gemini-2.5-flash"
    TEMPERATURE = 0.7
    apify_key = "apify_api_Di72i0OqHdbXT393VqlLIjCjEooyo51NiyqR"
