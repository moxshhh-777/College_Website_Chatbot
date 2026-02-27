import os
from dotenv import load_dotenv # API key and Ingest's source

from langchain_groq import ChatGroq # API KEY MODEL 
from langchain_community.vectorstores import FAISS 
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate # PROMPT Building / Constructing

load_dotenv()


def build_chain():

    # Loads embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Loads FAISS
    vectorstore = FAISS.load_local(
        "data/faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # GROQ API KEY 
    print(os.getenv("GROQ_API_KEY"))
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=os.getenv("GROQ_API_KEY")
    )

    prompt = ChatPromptTemplate.from_template("""
                                              
Use:
- Top 5 retrieved context , show them in answers only if it was asked by user's query. 
- remember the last 10 coversations , only answer the last recent 1 conversation if it was asked by user.
- Current user question at the top when you start giving answer.
- alwyas shows the data ("answer of the query") in point wise , start new sentence from new point.
                                               
Context:
{context}

Conversation History:
{history}

Question:
{question}

If answer not found in context, say:
"The Answer is not provided in system."
                                              
""")

    def run_chain(question: str, history: str):
        
        question = str(question)

       
        docs = retriever.invoke(question)

        context = "\n\n".join([doc.page_content for doc in docs])

        formatted_prompt = prompt.invoke({
            "context": context,
            "history": history,
            "question": question
        })

        response = llm.invoke(formatted_prompt)

        return response.content

    return run_chain
