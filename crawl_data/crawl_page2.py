import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from collections import deque
from urllib.parse import urljoin, urldefrag, urlparse, urlunparse

# Base URL
base_url = "https://www.haui.edu.vn"
visited_links = set()  # To avoid reprocessing the same link
links_data = []        # To store extracted links and titles
queue = deque([base_url])

# Function to get full URL from relative URL using urljoin
def get_full_url(relative_url, base=base_url):
    return urljoin(base, relative_url)

# Function to normalize URLs
def normalize_url(url):
    parsed = urlparse(url)
    # Remove fragment
    parsed = parsed._replace(fragment='')
    # Optionally, remove query parameters if they are not needed
    # parsed = parsed._replace(query='')
    # Remove trailing slash
    path = parsed.path.rstrip('/')
    parsed = parsed._replace(path=path)
    normalized = urlunparse(parsed)
    return normalized

# Function to extract category from the URL
def get_category_from_url(url):
    if '/vn/' in url:
        path = url.split('/vn/')[1]
        category = path.split('/')[0]
        return category
    return ""

# Function to scrape links and titles from a given page
def scrape_links_from_page(url):
    normalized_url = normalize_url(url)
    if normalized_url in visited_links:
        return  # Skip if the link is already processed
    
    print(f"Scraping: {normalized_url}")
    visited_links.add(normalized_url)
    
    try:
        # Send request to fetch the page content
        response = requests.get(normalized_url)
        response.raise_for_status()
        
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Define target selectors
        div_selectors = [
            '.irs-post-item a',    # for <div class="irs-post-item">
            '.othernews a',        # for <div class="othernews">
            '.irs-courses-col a',  # for <div class="irs-courses-col">
            '.entry a',            # for <div class="entry">
            'li.dropdown a'        # for <li class="dropdown">
        ]
        
        for selector in div_selectors:
            for link in soup.select(selector):
                href = link.get('href')
                if href:
                    full_url = get_full_url(href, base=normalized_url)
                    normalized_full_url = normalize_url(full_url)
                    title = link.get_text(strip=True)
                    category = get_category_from_url(normalized_full_url)
                    
                    # Avoid duplicates in links_data
                    if not any(d['url'] == normalized_full_url for d in links_data):
                        links_data.append({
                            'url': normalized_full_url,
                            'title': title,
                            'category': category
                        })
                    
                    # Only add to queue if within the same domain and not visited
                    if (normalized_full_url not in visited_links and
                        normalized_full_url.startswith(base_url)):
                        queue.append(normalized_full_url)
    
    except requests.RequestException as e:
        print(f"Error scraping {normalized_url}: {e}")
    
    time.sleep(1)  # Be polite to the server and avoid overloading it

# Function to start the scraping process
def start_scraping(max_links=300):
    processed = 0
    while queue and processed < max_links:
        current_url = queue.popleft()  # Get the next URL from the queue
        scrape_links_from_page(current_url)
        processed += 1
    
    # Saving the links and titles to a JSON file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"scraped_links_{timestamp}.json"
    
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(links_data, f, ensure_ascii=False, indent=4)
    
    print(f"Scraping finished. Data saved to {file_name}")

# Run the scraping
if __name__ == "__main__":
    start_scraping()