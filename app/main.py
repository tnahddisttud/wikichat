import uuid

import uvicorn
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
import logging
from chatbot import IntentClassifier, get_response
from db import VectorStore, CollectionNotCreatedError
from webloader import get_wikipedia_text
from schemas import WikiUrl, Message

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)

app = FastAPI(title="WikiChat: Your Friendly Information Retrieval Chatbot!")

vector_store = VectorStore()
intent_classifier = IntentClassifier()


@app.get('/')
def home():
    """
    Home endpoint to indicate the service is running.
    """
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/index_data", status_code=status.HTTP_201_CREATED)
def index_data(wiki_url: WikiUrl):
    """
    Endpoint to index Wikipedia data.

    Args:
        wiki_url (WikiUrl): The URL of the Wikipedia page to index.
    """
    logger.info("Fetching and processing content from the URL")
    data = get_wikipedia_text(wiki_url.url)
    collection_id = str(uuid.uuid4())
    logger.info("Indexing contexts in VectorDB")
    vector_store.create_collection(collection_id, data)
    logger.info("Database has been created successfully!")
    return Response(content="Database has been created successfully!", status_code=status.HTTP_201_CREATED)


@app.post("/chat", status_code=status.HTTP_200_OK)
def chat(message: Message):
    """
    Endpoint to handle chat messages.

    Args:
        message (Message): The user's message.

    Returns:
        Response: The chatbot's response.
    """
    user_message = message.message
    intent = intent_classifier.predict_intent(user_message)
    logger.info(f"User: {user_message}  | Intent: {intent}")
    if intent == 'wikipedia':
        try:
            response = vector_store.query(user_message)
        except CollectionNotCreatedError as e:
            response = "Please ensure that the database is created before asking your question."

    else:
        response = get_response(intent)
    logger.info(f"WikiBot: {response}")
    return JSONResponse(content={"message": response}, status_code=status.HTTP_200_OK)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8001, reload=True)
