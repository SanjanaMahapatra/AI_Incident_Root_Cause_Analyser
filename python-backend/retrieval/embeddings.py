from langchain_openai import OpenAIEmbeddings
import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("api key not found")

embeddings = OpenAIEmbeddings(api_key=api_key)