from langchain_neo4j import Neo4jVector
from typing import Dict, Any
import logging

from llm.get_graph import get_graph_function
from llm.get_llm import get_embedding_function

# Configure logging
logger = logging.getLogger(__name__)

class Neo4jChunkRetriever:
    """
    A class to manage Neo4j vector retrievers for different embedding models.
    """
    
    def __init__(self):
        self.graph = get_graph_function()
        self.embedding_functions = self._initialize_embedding_functions()
        self.neo4j_vector_indexes = {}
        self._create_available_indexes()
    
    def _initialize_embedding_functions(self) -> Dict[str, Any]:
        """Initialize available embedding functions."""
        return {
            'openai': get_embedding_function(),
            # Add other embedding functions here when needed
            # 'phobert': get_hugginface_embedding_phobert(),
            # 'keep': get_hugginface_embedding_keep()
        }
    
    @property
    def _retrieval_query(self) -> str:
        """Standard retrieval query for all indexes."""
        return """
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
    
    def _create_neo4j_vector_index(self, embedding_function: Any, index_name: str) -> Neo4jVector:
        """
        Create a Neo4j vector index with given embedding function.
        
        Args:
            embedding_function: The embedding function to use
            index_name: Name of the Neo4j index
            
        Returns:
            Neo4jVector instance
        """
        return Neo4jVector.from_existing_graph(
            embedding_function,
            graph=self.graph,
            index_name=index_name,
            node_label="Chunk",
            text_node_properties=["text"],
            embedding_node_property="content_embedding",
            retrieval_query=self._retrieval_query
        )
    
    def _create_available_indexes(self) -> None:
        """Create all available Neo4j vector indexes."""
        index_mapping = {
            'openai': 'embedding_openai',
            'phobert': 'embedding_phobert',
            'keep': 'embedding_keep'
        }
        
        for embedding_name, embedding_function in self.embedding_functions.items():
            try:
                index_name = index_mapping.get(embedding_name, f"embedding_{embedding_name}")
                self.neo4j_vector_indexes[embedding_name] = self._create_neo4j_vector_index(
                    embedding_function, 
                    index_name
                )
                logger.info(f"Successfully created '{embedding_name}' retriever.")
            except Exception as e:
                logger.error(f"Failed to create '{embedding_name}' index: {e}")
    
    def get_chunk_retriever(self, name: str, **search_kwargs):
        """
        Get a chunk retriever by embedding name.
        
        Args:
            name: Name of the embedding model ('openai', 'phobert', etc.)
            **search_kwargs: Additional search parameters
            
        Returns:
            Configured retriever instance
            
        Raises:
            ValueError: If the specified retriever name is not available
        """
        if name not in self.neo4j_vector_indexes:
            available_names = ', '.join(self.neo4j_vector_indexes.keys())
            raise ValueError(
                f"Retriever for '{name}' not found. Available names: {available_names}"
            )
        
        # Default search parameters
        default_search_kwargs = {
            'score_threshold': 0.5,
            'k': 5
        }
        default_search_kwargs.update(search_kwargs)
        
        return self.neo4j_vector_indexes[name].as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs=default_search_kwargs
        )
    
    @property
    def available_retrievers(self) -> list:
        """Get list of available retriever names."""
        return list(self.neo4j_vector_indexes.keys())


# Create singleton instance
_retriever_manager = Neo4jChunkRetriever()

# Public API functions for backward compatibility
def get_chunk_retriever(name: str, **search_kwargs):
    """
    Get a chunk retriever by embedding name.
    
    Args:
        name: Name of the embedding model
        **search_kwargs: Additional search parameters (score_threshold, k, etc.)
    
    Returns:
        Configured retriever instance
    """
    return _retriever_manager.get_chunk_retriever(name, **search_kwargs)

def get_available_retrievers() -> list:
    """Get list of available retriever names."""
    return _retriever_manager.available_retrievers

# Example usage:
# chunk_retriever_openai = get_chunk_retriever('openai')
# chunk_retriever_with_custom_params = get_chunk_retriever('openai', score_threshold=0.7, k=3)