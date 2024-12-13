from langchain.embeddings import OpenAIEmbeddings
from src.config.settings import settings

class EmbeddingManager:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            api_key=settings.OPENAI_API_KEY
        )
    
    async def get_embeddings(self, texts: list[str]):
        return await self.embeddings.aembed_documents(texts)