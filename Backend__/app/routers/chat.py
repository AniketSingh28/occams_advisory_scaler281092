# backend/app/routers/chat.py
from fastapi import APIRouter
from pydantic import BaseModel
import json, os, pickle, re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

router = APIRouter()

BASE = os.path.join(os.path.dirname(__file__), "..", "..", "..")
CHUNKS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "knowledge_chunks.json")
VEC_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "tfidf_vectorizer.pkl")

# Load knowledge base + vectorizer
chunks = json.load(open(CHUNKS_FILE, encoding="utf8")) if os.path.exists(CHUNKS_FILE) else []
vec = pickle.load(open(VEC_FILE, "rb")) if os.path.exists(VEC_FILE) else None

SIM_THRESHOLD = 0.15


class ChatIn(BaseModel):
    session_id: str
    message: str


# Very naive PII masking function
email_re = re.compile(r"[\w\.-]+@[\w\.-]+")
phone_re = re.compile(r"\+?[0-9][0-9\- ()]{5,20}")


def mask_pii(text: str) -> str:
    t = email_re.sub("<EMAIL_REDACTED>", text)
    t = phone_re.sub("<PHONE_REDACTED>", t)
    return t


@router.post("/query")
async def query_chat(req: ChatIn):
    q = mask_pii(req.message)

    # Fallback when no index available
    if not vec or not chunks:
        return {
            "answer": "I can't access the knowledge base right now. Please try later.",
            "sources": []
        }

    # Transform query
    qv = vec.transform([q])
    texts = [c["text"] for c in chunks]

    # Compute similarities
    X = vec.transform(texts)
    sims = cosine_similarity(qv, X)[0]

    top_idx = np.argmax(sims)
    top_score = float(sims[top_idx])

    if top_score < SIM_THRESHOLD:
        return {
            "answer": "I don't have that information in my Occams Advisory content.",
            "sources": []
        }

    # Prepare grounded response
    top_chunk = chunks[int(top_idx)]
    answer = f"According to the site: \"{top_chunk['text'][:400]}\""

    return {
        "answer": answer,
        "sources": [top_chunk["url"]],
        "score": top_score
    }
