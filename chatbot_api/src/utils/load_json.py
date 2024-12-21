from langchain_community.document_loaders import JSONLoader

import json
from pathlib import Path
from pprint import pprint
from langchain.text_splitter import RecursiveCharacterTextSplitter

def metadata_func(record: dict, metadata: dict) -> dict:
    metadata["source"] = record.get("source")
    metadata["title"] = record.get("title")

    return metadata


file_path='/Users/admin/Working/nckh-chatbot-neo4j/crawl_data/fit.jsonl'
def get_chunk_with_json(file_path):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 2000,
        chunk_overlap  = 500,
        length_function = len,
    )
    # loader = JSONLoader(
    #     file_path=file_path,
    #     jq_schema=".kwargs",
    #     content_key=".page_content",
    #     text_content=False,
    #     metadata_func=metadata_func,
    #     json_lines=True
    # )

    
    data = json.loads(Path(file_path).read_text())
    return data
    page_content = data[2]['kwargs']['page_content']
    pprint(page_content)
        
    title = data[2]['kwargs']['metadata']['title']
    source = data[2]['kwargs']['metadata']['source']
    chunks = text_splitter.split_text(page_content)
    print(chunks)
    # data = loader.load()
    # text_splitter.split_documents(data)
    # pprint(data[2])
    # pprint(data[1].metadata)
    # print(type(data))
    # print(type(data[0]))
    # chunks = text_splitter.split_documents(data)

    # print(chunks[3])

    # return data
    # page_content = data[2]['kwargs']['page_content']


get_chunk_with_json(file_path=file_path)