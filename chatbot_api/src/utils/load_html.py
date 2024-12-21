from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text_html(url):
    loader = WebBaseLoader(url, encoding='utf-8')

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap  = 300,
        length_function = len,
    )
    docs = loader.lazy_load()
    chunks = text_splitter.split_documents(docs)
    return chunks

url="https://fit.haui.edu.vn/vn/html/thong-tin-chung"
chunks = chunk_text_html(url)
# print(chunks)
print(chunks[0].metadata.get('page'))
print(chunks[0].page_content)

