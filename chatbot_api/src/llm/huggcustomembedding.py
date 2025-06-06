from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np

def get_hugginface_embedding_DVT():
    model = HuggingFaceEmbeddings(model_name="dangvantuan/vietnamese-embedding")
    return model

def get_hugginface_embedding_mpnet():
    model = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
    return model

def get_hugginface_embedding_phobert():
    model = HuggingFaceEmbeddings(model_name="vinai/phobert-base-v2")
    return model

def get_hugginface_embedding_allMini():
    model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return model

def get_hugginface_embedding_dotv1():
    model = HuggingFaceEmbeddings(model_name="multi-qa-mpnet-base-dot-v1")
    return model

def get_hugginface_embedding_bkai():
    model = HuggingFaceEmbeddings(model_name="bkai-foundation-models/vietnamese-bi-encoder")
    return model


def get_hugginface_embedding_keep():
    model = HuggingFaceEmbeddings(model_name="keepitreal/vietnamese-sbert")
    return model
# model = get_hugginface_embedding_keep()
# result = model.embed_query("Hi nice to meet you")
# print(result)
# print(len(result))
# print(np.shape(result))

