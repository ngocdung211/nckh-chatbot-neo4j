import json
from neo4j_client import Neo4jClient
from utils.load_html import chunk_text_html
from utils.load_json import get_chunk_with_json
import asyncio
from langchain.text_splitter import RecursiveCharacterTextSplitter

neo4j = Neo4jClient()

# Function to process a single URL
async def process_link(url, title, chunks):
    try:
        print(f"Processing: {url} - {title})")
        filename = title  # Use the title as the filename
        file_id = await neo4j.create_file_with_chunks(filename=filename, chunks=chunks, link=url)
        print(f"File created successfully for {url} with ID: {file_id}")
    except Exception as e:
        print(f"Failed to process {url}: {e}")

# Main function to loop through the JSON file
async def main(json_file):
    try:
        # Load the JSON file
        webs = get_chunk_with_json(json_file)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 2000,
            chunk_overlap  = 500,
            length_function = len,
        )
        # Loop through each entry in the JSON file
        tasks = []
        for i,data in enumerate(webs[1500:]):
            page_content = data['kwargs']['page_content']
            if len(page_content)>500:
                title = data['kwargs']['metadata']['title']
                source = data['kwargs']['metadata']['source']
                chunks = text_splitter.split_text(page_content)
                print("❌"*10)
                print(i)
                # Process each link asynchronously
                tasks.append(process_link(source, title, chunks))
        
        # Run all tasks concurrently
        await asyncio.gather(*tasks)
        print("All links processed successfully.")
    except Exception as e:
        print(f"Error while processing JSON file: {e}")

    

        # print(chunks)
        # print(title)
        # print(source)

        # process_link(url=source,title=title,chunks=chunks)

# Run the main function
if __name__ == "__main__":
    
    json_file = "/Users/admin/Working/nckh-chatbot-neo4j/crawl_data/haui.jsonl"  # Replace with your JSON file name

    asyncio.run(main(json_file))