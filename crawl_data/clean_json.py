import json
from urllib.parse import urlparse

# Function to clean and filter URLs
def clean_json_file(input_file, output_file):
    try:
        # Load the JSON data
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        cleaned_data = []
        unique_urls = set()

        for entry in data:
            url = entry.get("url", "")
            title = entry.get("title", "")
            category = entry.get("category", "")

            # Filter out invalid URLs (e.g., starting with "//")
            if not url.startswith("http"):
                print(f"Skipping invalid URL: {url}")
                continue

            # Remove duplicates using a set
            if url not in unique_urls:
                unique_urls.add(url)
                cleaned_data.append({
                    "url": url,
                    "title": title,
                    "category": category
                })

        # Save the cleaned JSON data
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_data, f, ensure_ascii=False, indent=4)

        print(f"Cleaned data saved to {output_file}")
        print(f"Total valid entries: {len(cleaned_data)}")

    except Exception as e:
        print(f"Error: {e}")

# Input and output file names
input_file = "/Users/admin/Working/nckh-chatbot-neo4j/crawl_data/scraped_links_20241220_180452.json"  # Replace with your input file name
output_file = "cleaned_links5.json"

# Run the cleaning function
clean_json_file(input_file, output_file)