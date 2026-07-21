"""
Module 2 + 3 - Xu ly van ban, xay chi muc, va chuan bi rank (TF-IDF)

Doc data/movies.json, ghep cac truong quan trong thanh 1 "document" van ban
cho moi phim, roi dung TfidfVectorizer (scikit-learn) de xay index.
Luu vectorizer + ma tran TF-IDF ra data/index.pkl de search.py dung lai
(khong can tinh lai moi lan tim kiem).

Cach dung:
    python build_index.py
"""
import json
import pickle
import re

from sklearn.feature_extraction.text import TfidfVectorizer

STOPWORDS_VI = {
    "va", "cua", "la", "mot", "nhung", "cho", "voi", "trong", "khong",
    "de", "co", "nay", "cac", "duoc", "tren", "khi", "sau", "the", "nguoi",
    "a", "an", "the", "of", "in", "to", "and", "is", "it", "on", "for",
}


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOPWORDS_VI]
    return " ".join(tokens)


def build_document(movie: dict) -> str:
    # Ten phim va the loai duoc lap lai (x3) de tang trong so tu nhien
    # khi dua vao TF-IDF chung, khong can code trong so thu cong rieng.
    parts = [
        (movie.get("title") or "") + " " + (movie.get("title") or "") + " " + (movie.get("title") or ""),
        " ".join(movie.get("genres", []) or []) * 2,
        movie.get("overview") or "",
    ]
    return clean_text(" ".join(parts))


def main():
    with open("data/movies.json", "r", encoding="utf-8") as f:
        movies = json.load(f)

    print(f"Dang xu ly {len(movies)} phim...")
    documents = [build_document(m) for m in movies]

    vectorizer = TfidfVectorizer(min_df=1)
    tfidf_matrix = vectorizer.fit_transform(documents)

    with open("data/index.pkl", "wb") as f:
        pickle.dump({
            "vectorizer": vectorizer,
            "tfidf_matrix": tfidf_matrix,
            "movies": movies,
        }, f)

    print(f"Da xay xong index: {tfidf_matrix.shape[0]} van ban, {tfidf_matrix.shape[1]} tu vung")
    print("Luu vao data/index.pkl")


if __name__ == "__main__":
    main()
