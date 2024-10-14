import requests
import random
import string
import sys
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_tor_session():
    session = requests.session()
    session.proxies = {'http':  'socks5h://127.0.0.1:9050',
                       'https': 'socks5h://127.0.0.1:9050'}
    return session

def save_content(content, url):
    filename = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    with open(f"{filename}.txt", "w+", encoding="utf-8") as file:
        file.write(f"URL: {url}\n\n")
        file.write(content)
    print(f"Saved content from {url} to {filename}.txt")

def extract_links(content, base_url):
    soup = BeautifulSoup(content, 'html.parser')
    return [urljoin(base_url, link.get('href')) for link in soup.find_all('a', href=True)]

def should_exclude(url, exclusion_rules):
    parsed_url = urlparse(url)
    path = parsed_url.path.lower()
    
    for rule in exclusion_rules:
        if rule in path:
            return True
    return False

def torSearcher(url, session, exclusion_rules, visited=None, depth=0, max_depth=1):
    if visited is None:
        visited = set()
    
    if depth > max_depth or url in visited or should_exclude(url, exclusion_rules):
        return
    
    visited.add(url)
    print(f"Scraping {url} (Depth: {depth})")
    
    try:
        response = session.get(url)
        content = response.text
        save_content(content, url)
        
        links = extract_links(content, url)
        for link in links:
            if link.startswith(url):  # Only follow links within the same domain
                torSearcher(link, session, exclusion_rules, visited, depth + 1, max_depth)
    except Exception as e:
        print(f"Error scraping {url}: {e}")

def main():
    session = get_tor_session()
    
    # Define exclusion rules
    exclusion_rules = ['/home', '/tags', '/contacts']
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as file:
            urls = [line.strip() for line in file]
    else: 
        urls = ["http://bianlianlbc5an4kgnay3opdemgcryg2kpfcbgczopmm3dnbz3uaunad.onion/companies/"]
    
    for url in urls:
        if not url.startswith("http"):
            url = "http://" + url
        torSearcher(url, session, exclusion_rules)

if __name__ == "__main__":
    main()