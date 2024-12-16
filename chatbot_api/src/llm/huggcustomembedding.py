from langchain_huggingface import HuggingFaceEmbeddings

class CustomEmbeddingModel:
    def __init__(self, model_name):
        self.model = HuggingFaceEmbeddings(model_name=model_name)

    def get_embeddings(self, sentences):
        print("Available methods:", dir(self.model))  # Check available methods
        return self.model.embed_documents(sentences)  # Use the embed method to get embeddings

# Usage
# embedding_model = CustomEmbeddingModel('dangvantuan/vietnamese-embedding')
embedding_model = CustomEmbeddingModel('sentence-transformers/bert-base-nli-cls-token')
print("Available methods:", dir(embedding_model))  # Check available methods
embeddings = embedding_model.get_embeddings(["Hello world!", "This is a test."])
print(embeddings)