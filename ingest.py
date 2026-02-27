import os
import json # for storing the scraped DATA
import requests # for sending the Request to scraps the HTTPs URLs
from bs4 import BeautifulSoup # this library is used to parsing the HTML data from webpages
from urllib.parse import urljoin, urlparse # filters the URL during scrapping
from dotenv import load_dotenv # API KEY is HERE

from langchain_community.vectorstores import FAISS # stored the Embeddings Data in FAISS (vector)
from langchain_text_splitters import RecursiveCharacterTextSplitter # Reduces the chunk size 
from langchain_huggingface import HuggingFaceEmbeddings # Converts the chunks into Vector 


load_dotenv() 

BASE_URL = "https://dcpateleducampus.in/"

EXCLUDED_EXTENSIONS = (
    ".pdf", ".jpg", ".jpeg", ".png",
    ".gif", ".svg", ".mp4", ".avi", ".mov"
)

EXCLUDED_KEYWORDS = (
    "news", "event", "gallery",
    "video", "image", "uploads"
)

visited = set()
scraped_data = []
page_count = 0



def is_valid_url(url):
    parsed = urlparse(url)

    if parsed.netloc != urlparse(BASE_URL).netloc:
        return False

    if any(url.lower().endswith(ext) for ext in EXCLUDED_EXTENSIONS):
        return False

    if any(keyword in url.lower() for keyword in EXCLUDED_KEYWORDS):
        return False

    return True



def scrape_website(url, depth=0):
    global page_count

    if url in visited:
        return

    visited.add(url)
    indent = "  " * depth

    print(f"{indent} Scraping: {url}")

    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(separator=" ", strip=True)

        scraped_data.append({
            "url": url,
            "content": text
        })

        page_count += 1
        print(f"{indent}Success | Pages Scraped: {page_count}")

        
        for link in soup.find_all("a", href=True):
            next_url = urljoin(url, link["href"])

            if is_valid_url(next_url):
                scrape_website(next_url, depth + 1)

    except Exception as e:
        print(f"{indent} Error scraping {url}")
        print(f"{indent}   Reason: {e}")


if __name__ == "__main__":

    
    scrape_website(BASE_URL)
    os.makedirs("data", exist_ok=True)

    with open("data/scraped_data.json", "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, indent=4)

    print(f" Total Pages Scraped: {page_count}")
    documents = [item["content"] for item in scraped_data]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.create_documents(documents)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2" # Model is used for Vector creation 
    )

    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("data/faiss_index")

    print("\n Scrapping Completed ! ")
