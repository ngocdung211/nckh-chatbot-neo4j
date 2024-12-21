import requests
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urlparse

# Base URL for the website
BASE_URL = "https://fit.haui.edu.vn/vn"

# Function to get links from a single page
def get_links_from_page(url, driver=None):
    try:
        if driver:
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, "html.parser")
        else:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
        
        links = []
        
        # Extract links from <a> tags with href attributes
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            # Make the link absolute by joining it with the base URL
            full_url = urljoin(BASE_URL, href)
            title = a_tag.get_text(strip=True)
            links.append({"url": full_url, "title": title, "category": "unknown"})
        
        return links
    except Exception as e:
        print(f"Error while scraping {url}: {e}")
        return []

# Function to recursively crawl links
def crawl_links(start_url, depth=2, visited=set(), driver=None):
    if depth == 0 or start_url in visited:
        return []
    
    visited.add(start_url)
    
    # Get links from the current page
    links = get_links_from_page(start_url, driver)
    
    # Recursively crawl through all links found
    all_links = []
    for link in links:
        all_links.append(link)
        all_links.extend(crawl_links(link["url"], depth - 1, visited, driver))
    
    return all_links

# Function to save links to a JSON file
def save_links_to_json(links, filename="scraped_links.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(links, f, ensure_ascii=False, indent=4)

# Main function
def main():
    # Timestamp for unique filename
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_filename = f"scraped_links_{timestamp}.json"
    
    # Setup Selenium WebDriver (for pages requiring JS rendering)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Start crawling from the base URL
    crawled_links = crawl_links(BASE_URL, depth=2, driver=driver)
    
    # Save the results to a JSON file
    save_links_to_json(crawled_links, output_filename)
    print(f"Scraped data saved to {output_filename}")

    # Close the Selenium driver
    driver.quit()

if __name__ == "__main__":
    main()