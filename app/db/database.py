import os
from pathlib import Path
from typing import List
from uuid import uuid4

import chromadb
from chromadb import Settings

# Determine the absolute path to the vectorstore
vectorstore_path = Path(__file__).parent.parent.absolute() / "vectorstore"

# Initialize the ChromaDB client
chroma_client = chromadb.PersistentClient(path=os.path.normpath(vectorstore_path),
                                          settings=Settings(anonymized_telemetry=False, allow_reset=True))


class CollectionNotCreatedError(Exception):
    """Exception raised when attempting to query without creating a collection."""
    pass


class VectorStore:
    def __init__(self):
        self.collection = None

    def create_collection(self, collection_name: str, sentences: List[str]):
        """
        Create a collection in ChromaDB and add documents to it.

        Args:
            collection_name (str): The name of the collection.
            sentences (List[str]): List of sentences to add as documents.
        """
        chroma_client.reset()
        document_ids = [str(uuid4()) for _ in range(len(sentences))]
        collection = chroma_client.create_collection(name=collection_name)
        collection.add(documents=sentences, ids=document_ids)
        self.collection = collection

    def query(self, question: str) -> str:
        """
        Query the collection for a given question.

        Args:
            question (str): The question to query for.

        Returns:
            str: The response to the query.
        """
        if not self.collection:
            raise CollectionNotCreatedError("Collection has not been created yet.")

        response = self.collection.query(query_texts=[question], n_results=1)
        documents = response.get('documents')
        if documents:
            return documents[0][0]
        return "Apologies, I didn't catch that. Could you please provide more specific details?"
