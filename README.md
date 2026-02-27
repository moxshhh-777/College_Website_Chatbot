SUMMARY of this PROJECT :

-Developed a Retrieval-Augmented Generation (RAG) chatbot that answers queries based on real college website data.
-Implemented a recursive web scraper using requests and BeautifulSoup to extract and clean textual content while filtering irrelevant media and links.
-Stored scraped content in structured JSON format and processed it into semantic chunks for efficient retrieval.
-Generated vector embeddings using HuggingFace sentence-transformers and stored them in a FAISS vector database for fast similarity search.
-Designed a retrieval pipeline that fetches the top 5 most relevant context chunks for each user query.
-Integrated Groq LLM (Llama 3) to generate context-aware responses strictly grounded in retrieved data.
-Built a modular backend using FastAPI, exposing REST APIs for chatbot interaction and scalable integration.
-Developed an elegant conversational interface using Streamlit with gradient styling and chat bubble UI for improved user experience.
-Implemented conversation memory to include the last 10 chat messages, enhancing contextual continuity.
-Added fallback logic to return a controlled response when information is not present in the knowledge base.
-Structured the project with clear separation of ingestion, retrieval, API, and UI layers to follow production-style architecture.
-Demonstrates practical understanding of RAG systems, vector databases, semantic search, prompt engineering, and full-stack AI application development.

PROBLEM faced :

-Langchain and Langchian's Library versions were not matching.
-While Scraping the URL , it was taking very long time so-- I excluded the non-important extensions & Keywords like (.png , .jpg , .pdf , news , video , gallery etc.).
-API key not found error.
-Backend error-- 500 , 404 , 401 not found , "Dict" has no attribute "replaced" error. (fixed that by locating the scraped json data).
-prompt mistakes in PromptTemplate 
-Sentence transformer (for vector Creation) model name mistake.
-Github minor Login error (fixed by "git pull" ReadME file).
