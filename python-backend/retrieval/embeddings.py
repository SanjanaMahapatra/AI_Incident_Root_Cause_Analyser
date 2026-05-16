from langchain_openai import OpenAIEmbeddings
import os

embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))