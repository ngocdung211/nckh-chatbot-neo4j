import os
from langchain_neo4j import Neo4jVector
from llm.get_graph import get_graph_function
from llm.get_llm import get_embedding_function
# from llm.huggcustomembedding import (
#     # get_hugginface_embedding_DVT, 
#     # get_hugginface_embedding_phobert, 
#     # get_hugginface_embedding_allMini, 
#     # get_hugginface_embedding_basev2,
#     # get_hugginface_embedding_dotv1
# )

# Initialize graph and embeddings
graph = get_graph_function()
embedding_functions = {
    'openai': get_embedding_function(),
    # 'dvt': get_hugginface_embedding_DVT(),
    # 'phobert': get_hugginface_embedding_phobert(),
    # 'allMini': get_hugginface_embedding_allMini(),
    # 'basev2': get_hugginface_embedding_basev2(),
    # 'dotv1': get_hugginface_embedding_dotv1(),
}

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
neo4j_vector_indexes = {
    'openai': create_neo4j_vector_index(embedding_functions['openai'], "embedding_openai", "text_embedding_openai"),
    # 'dvt': create_neo4j_vector_index(embedding_functions['dvt'], "embedding_DVT", "text_embedding_DVT"),
    # 'phobert': create_neo4j_vector_index(embedding_functions['phobert'], "embedding_phobert", "text_embedding_phobert"),
    # 'dotv1': create_neo4j_vector_index(embedding_functions['dotv1'], "embedding_dov1", "text_embedding_dotv1t"),
    # 'allMini': create_neo4j_vector_index(embedding_functions['allMini'], "embedding_allMini", "text_embedding_allMini"),
    # 'basev2': create_neo4j_vector_index(embedding_functions['basev2'], "embedding_basev2", "text_embedding_basev2")
}

# Function to create a chunk retriever based on embedding name
def get_chunk_retriever(name):
    if name in neo4j_vector_indexes:
        return neo4j_vector_indexes[name].as_retriever(search_type="similarity_score_threshold", search_kwargs={'score_threshold': 0.7})
    else:
        raise ValueError(f"Retriever for '{name}' not found. Available names: {', '.join(neo4j_vector_indexes.keys())}")
# Example usage:
# To get the retriever for OpenAI:
# chunk_retriever_openai = get_chunk_retriever('openai')