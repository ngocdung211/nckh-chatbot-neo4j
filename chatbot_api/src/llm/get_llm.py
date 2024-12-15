from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
import os

# Load environment variables once
if load_dotenv(".env"):
    print("✅✅Environment file in llm loaded successfully")
else:
    print("❌❌Environment file in llm failed to load")

def get_embedding_function():

    print("get_embedding_function")
    api_key = os.getenv('OPENAI_API_KEY')
    embedding_model_name = os.getenv('OPENAI_EMBEDDING')
    if not api_key or not embedding_model_name:
        raise ValueError("Missing 'OPENAI_API_KEY' or 'OPENAI_EMBEDDING' in environment.")

    # Create and return the embeddings object
    embeddings = OpenAIEmbeddings(
        openai_api_key=api_key,
        model=embedding_model_name
    )
    return embeddings

def get_model_function():
    # Retrieve necessary environment variables
    print("get llm ")
    api_key = os.getenv('OPENAI_API_KEY')
    model_name = os.getenv('AGENT_MODEL')
    if not api_key or not model_name:
        raise ValueError("Missing 'OPENAI_API_KEY' or 'AGENT_MODEL' in environment.")

    # Create and return the chat model object
    model = ChatOpenAI(
        openai_api_key=api_key,
        model=model_name,
        temperature=0,
    )
    return model

def generate_test_model_function():
    # Retrieve necessary environment variables
    print("get llm ")
    api_key = os.getenv('OPENAI_API_KEY')
    model_name = os.getenv('TEST_MODEL')
    if not api_key or not model_name:
        raise ValueError("Missing 'OPENAI_API_KEY' or 'TETST_MODEL' in environment.")

    # Create and return the chat model object
    model = ChatOpenAI(
        openai_api_key=api_key,
        model=model_name,
        temperature=0,
    )
    return model

def get_eval_model_function():
    # Retrieve necessary environment variables
    print("get llm ")
    api_key = os.getenv('OPENAI_API_KEY')
    model_name = os.getenv('AGENT_MODEL')
    if not api_key or not model_name:
        raise ValueError("Missing 'OPENAI_API_KEY' or 'AGENT_MODEL' in environment.")

    # Create and return the chat model object
    model = ChatOpenAI(
        openai_api_key=api_key,
        model='gpt-4o',
        temperature=0,
    )
    return model

