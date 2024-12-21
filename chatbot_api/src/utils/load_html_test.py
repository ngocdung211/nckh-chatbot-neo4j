from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_document_web(url):
    loader = WebBaseLoader(url, encoding='utf-8')

    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size = 2000,
    #     chunk_overlap  = 300,
    #     length_function = len,
    # )
    docs = loader.load()
    return docs

# url="https://fit.haui.edu.vn/vn/html/thong-tin-chung"
# chunks = chunk_text_html(url)
# print(chunks[0].page_content)
# print(chunks.metadata.get('page'))
# print(chunks.page_content)

