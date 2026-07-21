"""
Module 3 - Truy van & Xep hang ket qua

Ham search(query, top_k) tra ve danh sach phim phu hop nhat, xep hang theo
diem cosine similarity giua query va document (da duoc TF-IDF hoa).
Dung lai chung mot index.pkl duoc build_index.py tao san.
"""
import pickle

from sklearn.metrics.pairwise import cosine_similarity

from build_index import clean_text

_CACHE = {}


def _load_index():
    if "data" not in _CACHE:
        with open("data/index.pkl", "rb") as f:
            _CACHE["data"] = pickle.load(f)
    return _CACHE["data"]


def search(query: str, top_k: int = 10) -> list:
    idx = _load_index()
    vectorizer = idx["vectorizer"]
    tfidf_matrix = idx["tfidf_matrix"]
    movies = idx["movies"]

    q_clean = clean_text(query)
    q_vec = vectorizer.transform([q_clean])

    scores = cosine_similarity(q_vec, tfidf_matrix).flatten()
    ranked_idx = scores.argsort()[::-1][:top_k]

    results = []
    for i in ranked_idx:
        if scores[i] <= 0:
            continue
        movie = dict(movies[i])
        movie["score"] = float(scores[i])
        results.append(movie)
    return results


if __name__ == "__main__":
    import sys
    q = " ".join(sys.argv[1:]) or "phim hanh dong"
    for r in search(q, top_k=10):
        print(f"{r['score']:.3f}  {r['title']}  ({r.get('release_date', '')})")
