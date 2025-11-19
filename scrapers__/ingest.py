import json, os, math, pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_IN = os.path.join(os.path.dirname(__file__), "..", "data", "occams_pages.json")
OUT_CHUNKS = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge_chunks.json")
OUT_VEC = os.path.join(os.path.dirname(__file__), "..", "data", "tfidf_vectorizer.pkl")

os.makedirs(os.path.dirname(OUT_CHUNKS), exist_ok=True)

pages = json.load(open(DATA_IN, encoding="utf8"))

# naive chunk by paragraph
chunks = []
chunk_id = 0

for p in pages:
    for para in p["text"].split("\n\n"):
        para = para.strip()
        if len(para) < 50:
            continue

        chunk = {
            "id": chunk_id,
            "text": para,
            "url": p["url"],
            "title": p.get("title", "")
        }

        chunks.append(chunk)
        chunk_id += 1

texts = [c["text"] for c in chunks]

if not texts:
    raise SystemExit("No texts found; run scraper first")

vec = TfidfVectorizer(stop_words='english', max_features=5000)
X = vec.fit_transform(texts)

# Save vectorizer and chunks
with open(OUT_VEC, "wb") as f:
    pickle.dump(vec, f)

with open(OUT_CHUNKS, "w", encoding="utf8") as f:
    json.dump(chunks, f, indent=2, ensure_ascii=False)

print("wrote", OUT_CHUNKS)
print("wrote", OUT_VEC)
