import os
from langchain_neo4j import Neo4jVector
from llm.get_graph import get_graph_function
from llm.get_llm import get_embedding_function
from llm.huggcustomembedding import (
    get_hugginface_embedding_phobert,
)

# Initialize graph and embeddings
graph = get_graph_function()

embedding_functions = {
    'openai': get_embedding_function(),
    'phobert': get_hugginface_embedding_phobert()
}

print("Available embedding functions:", embedding_functions.keys())

# Common retrieval query template
retrieval_query = """
RETURN score,
{
    content: node.text,
    next_contents: [(node)-[:HAS_PREV]->(nextChunk) | nextChunk.text]
} AS text,

{
    data: node.id,
    filename: [(file)-[:HAS_CHUNK]->(node) | file.filename],
    link: [(file)-[:HAS_CHUNK]->(node) | file.link],
    page_number: node.page_number
} AS metadata
"""

# Function to create a Neo4j vector index
def create_neo4j_vector_index(embedding_function, index_name, embedding_property):
    return Neo4jVector.from_existing_graph(
        embedding_function,
        graph=graph,
        index_name=index_name,
        node_label="Chunk",
        text_node_properties=["text"],
        embedding_node_property=embedding_property,
        retrieval_query=retrieval_query
    )

# Create all the Neo4jVector indexes dynamically
neo4j_vector_indexes = {}

try:
    neo4j_vector_indexes['openai'] = create_neo4j_vector_index(
        embedding_functions['openai'], 
        "embedding_openai", 
        "text_embedding_openai"
    )
    print("Created 'openai' retriever.")
except Exception as e:
    print(f"Failed to create 'openai' index: {e}")

try:
    neo4j_vector_indexes['phobert'] = create_neo4j_vector_index(
        embedding_functions['phobert'], 
        "embedding_phobert", 
        "text_embedding_phobert"
    )
    print("Created 'phobert' retriever.")
except Exception as e:
    print(f"Failed to create 'phobert' index: {e}")

print("Available retrievers:", neo4j_vector_indexes.keys())

# Function to create a chunk retriever based on embedding name
def get_chunk_retriever(name):
    if name in neo4j_vector_indexes:
        return neo4j_vector_indexes[name].as_retriever(
            search_type="similarity_score_threshold", 
            search_kwargs={'score_threshold': 0.7, 'k':2}
        )
    else:
        raise ValueError(
            f"Retriever for '{name}' not found. Available names: {', '.join(neo4j_vector_indexes.keys())}"
        )

# Example usage:
# To get the retriever for OpenAI:
# chunk_retriever_openai = get_chunk_retriever('openai')

# To get the retriever for PhoBERT:
# chunk_retriever_phobert = get_chunk_retriever('phobert')