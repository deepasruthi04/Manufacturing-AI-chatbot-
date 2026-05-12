import os
import glob
from pathlib import Path
from pypdf import PdfReader
from app.db.chroma import chromadb_client
from app.core.config import settings

CHUNK_SIZE = 600
CHUNK_OVERLAP = 100

def _load_pdfs() -> list[dict]:
    docs = []
    rag_dir = Path(settings.DOCUMENTS_PATH)
    pdf_paths = glob.glob(str(rag_dir / "*.pdf"))
    for pdf_path in pdf_paths:
        try:
            reader = PdfReader(pdf_path)
            full_text = "\n".join(
                page.extract_text() or "" for page in reader.pages
            ).strip()
            if full_text:
                docs.append({"text": full_text, "source": os.path.basename(pdf_path)})
        except Exception as e:
            print(f"[RAG] Failed to read {pdf_path}: {e}")
    return docs

def _chunk_text(text: str, source: str) -> list[dict]:
    chunks = []
    start = 0
    idx = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()
        if chunk:
            chunks.append({
                "id": f"{source}_{idx}",
                "text": chunk,
                "source": source,
            })
            idx += 1
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks

def build_vector_store(force_rebuild: bool = False):
    collection = chromadb_client.get_collection()
    
    if collection.count() > 0 and not force_rebuild:
        return collection

    if force_rebuild:
        chromadb_client.client.delete_collection(chromadb_client.collection_name)
        collection = chromadb_client.get_collection()

    docs = _load_pdfs()
    if not docs:
        return collection

    all_chunks = []
    for doc in docs:
        all_chunks.extend(_chunk_text(doc["text"], doc["source"]))

    ids = [c["id"] for c in all_chunks]
    texts = [c["text"] for c in all_chunks]
    metadatas = [{"source": c["source"]} for c in all_chunks]

    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        collection.add(
            ids=ids[i : i + batch_size],
            documents=texts[i : i + batch_size],
            metadatas=metadatas[i : i + batch_size],
        )
    return collection

def query_rag(question: str, top_k: int = 4) -> str:
    collection = chromadb_client.get_collection()
    if collection.count() == 0:
        # Try to build if empty
        collection = build_vector_store()
        if collection.count() == 0:
            return "No RAG documents are available."

    results = collection.query(
        query_texts=[question],
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    passages = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        relevance = round(1 - dist, 3)
        passages.append(
            f"[Source: {meta['source']} | Relevance: {relevance}]\n{doc}"
        )

    return "\n\n---\n\n".join(passages)
