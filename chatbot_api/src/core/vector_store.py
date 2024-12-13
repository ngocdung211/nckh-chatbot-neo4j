from langchain.vectorstores import Chroma
from src.core.embeddings import EmbeddingManager

class VectorStoreManager:
    def __init__(self, embedding_manager: EmbeddingManager):
        self.embedding_manager = embedding_manager
        self.vector_store = None
    
    async def init_store(self, texts: list[str]):
        self.vector_store = await Chroma.afrom_texts(
            texts=texts,
            embedding=self.embedding_manager.embeddings
        )
    
    async def similarity_search(self, query: str, k: int = 3):
        if not self.vector_store:
            return []
        return await self.vector_store.asimilarity_search(query, k=k)