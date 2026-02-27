import os
import json
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

BASE_URL = "https://dcpateleducampus.in/"

EXCLUDED_EXTENSIONS = (
    ".pdf", ".jpg", ".jpeg", ".png",
    ".gif", ".svg", ".mp4", ".avi", ".mov",
)

EXCLUDED_KEYWORDS = (
    "news", "event", "gallery",
    "video", "image", "uploads"
)


class WebsiteScraper:

    def __init__(self):
        self.visited = set()
        self.scraped_data = []
        self.page_count = 0
        os.makedirs("data", exist_ok=True)

    
    def normalize_url(self, url):
        parsed = urlparse(url)

        
        clean = parsed._replace(fragment="", query="")
        return clean.geturl().rstrip("/")

    
    def is_html_page(self, url):
        if any(url.lower().endswith(ext) for ext in EXCLUDED_EXTENSIONS):
            return False

        if any(keyword in url.lower() for keyword in EXCLUDED_KEYWORDS):
            return False

        if urlparse(url).netloc != urlparse(BASE_URL).netloc:
            return False

        return True


    def scrape_page(self, url):

        url = self.normalize_url(url)

        if url in self.visited:
            return []

        self.visited.add(url)

        print(f"\n Scraping: {url}")
        start = time.time()

        try:
            res = requests.get(url, timeout=8)
            res.raise_for_status()

            # Only HTML response
            if "text/html" not in res.headers.get("Content-Type", ""):
                return []

            soup = BeautifulSoup(res.text, "html.parser")
            text = soup.get_text(separator=" ", strip=True)

            duration = round(time.time() - start, 2)
            print(f" Time taken: {duration}s")

            self.scraped_data.append({
                "url": url,
                "content": text,
                "scraped_time": str(datetime.now()),
                "duration": duration,
                "page_count": self.page_count
            })

            self.page_count += 1

            links = []
            for tag in soup.find_all("a", href=True):
                next_url = urljoin(url, tag["href"])
                next_url = self.normalize_url(next_url)

                if self.is_html_page(next_url) and next_url not in self.visited:
                    links.append(next_url)

            return links

        except Exception as e:
            print(" Error:", e)
            return []


    def crawl(self):
        queue = [BASE_URL]

        while queue:
            url = queue.pop(0)
            new_links = self.scrape_page(url)
   
            for link in new_links:
                if link not in self.visited:
                    queue.append(link)



    def save_data(self):
        with open("data/scraped_data.json", "w", encoding="utf-8") as f:
            json.dump(self.scraped_data, f, indent=4)

        print(f"\n Pages scraped: {self.page_count}")


    def build_faiss(self):
        texts = [item["content"] for item in self.scraped_data]

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        docs = splitter.create_documents(texts)

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local("data/faiss_index")

        print(" FAISS Created")


if __name__ == "__main__":
    scraper = WebsiteScraper()
    scraper.crawl()
    scraper.save_data()
    scraper.build_faiss()