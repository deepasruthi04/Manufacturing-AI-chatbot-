import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
from app.core.config import settings
from pathlib import Path

class ChromaDB:
    def __init__(self):
        persist_dir = settings.CHROMA_PERSIST_DIRECTORY
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.embed_fn = DefaultEmbeddingFunction()
        self.collection_name = "manufacturing_rag"

    def get_collection(self):
        return self.client.get_or_create_collection(
            name=self.collection_name, 
            embedding_function=self.embed_fn
        )

chromadb_client = ChromaDB()
