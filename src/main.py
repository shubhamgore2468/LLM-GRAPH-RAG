import os
import sys
import json
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from src.data_processing.preprocess import preprocess_document
from src.models.createGraph import add_data_to_graph
from src.inference.langchain_integration import chain

# Set up logging

# Add the project root to Python path to ensure proper imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from scripts.getData import crawlAI
from src.logging_config import setup_logging
setup_logging()
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Global state
ANALYSIS_COMPLETE = False
CHAT_HISTORY = []
JSON_DATA = {}

# Request/Response Models
class URLRequest(BaseModel):
    url1: str
    url2: str

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    role: str
    content: str

@app.get("/")
def root():
    return {"message": "FastAPI backend for product review analysis"}

@app.post("/urls")
async def analyze_urls(payload: URLRequest):
    global ANALYSIS_COMPLETE, JSON_DATA

    urls = [payload.url1, payload.url2]
    JSON_DATA = {}

    try:
        for url in urls:
            logger.info(f"Crawling URL: {url}")
            crawlAI(url, JSON_DATA)
            logger.info("Crawling complete")

        # Optionally write to disk
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'crawl_new.json')
        with open(data_path, "w") as json_file:
            json.dump(JSON_DATA, json_file, indent=4)

        documents = preprocess_document(JSON_DATA)
        add_data_to_graph(documents)

        ANALYSIS_COMPLETE = True
        return {"status": "success", "message": "Analysis complete. You can now ask questions."}

    except Exception as e:
        logger.error(f"Error in /urls: {e}")
        raise HTTPException(status_code=500, detail=f"Error analyzing URLs: {e}")

@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    global CHAT_HISTORY, ANALYSIS_COMPLETE

    if not ANALYSIS_COMPLETE:
        raise HTTPException(status_code=400, detail="Please analyze URLs before chatting.")

    user_msg = {"role": "user", "content": payload.prompt}
    CHAT_HISTORY.append(user_msg)

    try:
        response = chain.invoke({"question": payload.prompt})
        assistant_msg = {"role": "assistant", "content": response}
        CHAT_HISTORY.append(assistant_msg)
        return assistant_msg

    except Exception as e:
        logger.error(f"Error in /chat: {e}")
        error_msg = f"An error occurred while processing your question: {e}"
        assistant_msg = {"role": "assistant", "content": error_msg}
        CHAT_HISTORY.append(assistant_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@app.post("/reset")
def reset_state():
    global ANALYSIS_COMPLETE, CHAT_HISTORY, JSON_DATA
    ANALYSIS_COMPLETE = False
    CHAT_HISTORY = []
    JSON_DATA = {}
    return {"status": "reset", "message": "Session reset successful"}
