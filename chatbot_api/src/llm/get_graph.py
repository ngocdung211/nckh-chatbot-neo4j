from langchain_community.graphs import Neo4jGraph
from langchain_neo4j import Neo4jGraph
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
if load_dotenv(".env"):
    print("✅✅Environment file in graph loaded successfully")
else:
    print("❌❌Environment file failed to load")

def get_graph_function():
    print("get graph")
    # Retrieve necessary environment variables
    graph_url = os.getenv("NEO4J_URI")
    graph_username = os.getenv("NEO4J_USERNAME")
    graph_password = os.getenv("NEO4J_PASSWORD")
    if not graph_url or not graph_username or  not graph_password:
        raise ValueError("Missing 'NEO4J_URI' or 'NEO4J_USERNAME' or 'NEO4J_PASSWORD' in environment.")

    # Create and return the chat model object
    graph = Neo4jGraph(
            url=graph_url,
            username=graph_username,
            password=graph_password,
            enhanced_schema=True
        )
    return graph