import json
from neo4j_client import Neo4jClient
from utils.load_html import chunk_text_html
import asyncio

neo4j = Neo4jClient()

# Function to process a single URL
async def process_link(url, title, category):
    try:
        print(f"Processing: {url} - {title} ({category})")
        chunks = chunk_text_html(url)  # Extract content in chunks
        filename = title  # Use the title as the filename
        file_id = await neo4j.create_file_with_chunks(filename=filename, chunks=chunks, link=url)
        print(f"File created successfully for {url} with ID: {file_id}")
    except Exception as e:
        print(f"Failed to process {url}: {e}")

# Main function to loop through the JSON file
async def main(json_file):
    try:
        # Load the JSON file
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Loop through each entry in the JSON file
        tasks = []
        for entry in data:
            url = entry.get("url")
            title = entry.get("title", "Unknown Title")
            category = entry.get("category", "Uncategorized")
            
            # Process each link asynchronously
            tasks.append(process_link(url, title, category))
        
        # Run all tasks concurrently
        await asyncio.gather(*tasks)
        print("All links processed successfully.")
    except Exception as e:
        print(f"Error while processing JSON file: {e}")

# Run the main function
if __name__ == "__main__":
    json_file = "/Users/admin/Working/nckh-chatbot-neo4j/crawl_data/scraped_links_20241220_175553.json"  # Replace with your JSON file name
    asyncio.run(main(json_file))