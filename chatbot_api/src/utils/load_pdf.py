from langchain_community.document_loaders import PDFPlumberLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(filename):
    loader = PDFPlumberLoader(filename)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1300,
        chunk_overlap  = 200,
        length_function = len,
    )
    docs = loader.lazy_load()
    chunks = text_splitter.split_documents(docs)
    return chunks

filename="/Users/admin/Downloads/Hướng dẫn, quy chế các danh hiệu phong trào/02 CT_Chuong trinh cong tac HSV 2024 - 2025.pdf"
chunks = chunk_text(filename)

print(chunks[0].metadata['page'])
print(chunks[0].metadata['CreationDate'])
print(chunks[0].page_content)

