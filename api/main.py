from fastapi import FastAPI # Server used ffor searching the retrieved data from json and loads it into STreamlit
from pydantic import BaseModel 
from chain import build_chain #


app = FastAPI()
chat_function = build_chain()


class ChatRequest(BaseModel):
    question: str
    history: str


@app.get("/")
def home():
    return {"message": " Chatbot API is running ---"}

@app.post("/chat")
async def chat(request: ChatRequest):
    answer = chat_function(request.question, request.history)
    return {"response": answer}


