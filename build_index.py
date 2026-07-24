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

# Ban dich the loai Viet -> Anh de ho tro tim kiem song ngu
GENRE_EN_MAP = {
    "Phim Hành Động": "action",
    "Phim Phiêu Lưu": "adventure",
    "Phim Hoạt Hình": "animation animated cartoon",
    "Phim Hài": "comedy funny humor",
    "Phim Chính Kịch": "drama",
    "Phim Tài Liệu": "documentary",
    "Phim Gia Đình": "family",
    "Phim Giả Tượng": "fantasy",
    "Phim Lịch Sử": "history historical",
    "Phim Kinh Dị": "horror scary",
    "Phim Nhạc": "music musical",
    "Phim Bí Ẩn": "mystery",
    "Phim Lãng Mạn": "romance romantic love",
    "Phim Khoa Học Viễn Tưởng": "science fiction sci-fi scifi",
    "Phim Gây Cấn": "thriller suspense",
    "Phim Chiến Tranh": "war",
    "Phim Miền Tây": "western",
    "Phim Hình Sự": "crime criminal",
    "Chương Trình Truyền Hình": "tv show television",
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
    # Them original_title (tieng Anh) va ban dich the loai de ho tro song ngu.
    title_vi = movie.get("title") or ""
    title_en = movie.get("original_title") or ""
    genres = movie.get("genres", []) or []
    genres_vi = " ".join(genres)
    genres_en = " ".join(GENRE_EN_MAP.get(g, "") for g in genres)

    parts = [
        # Title tieng Viet + tieng Anh, lap lai x3 de tang trong so
        (title_vi + " ") * 3 + (title_en + " ") * 3,
        # The loai ca tieng Viet lan tieng Anh, lap lai x2
        (genres_vi + " " + genres_en + " ") * 2,
        movie.get("overview") or "",
    ]
    return clean_text(" ".join(parts))


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MOVIES_PATH = DATA_DIR / "movies.json"
INDEX_PATH  = DATA_DIR / "index.pkl"


def main():
    if not MOVIES_PATH.exists():
        raise FileNotFoundError(
            f"Khong tim thay file du lieu tai: {MOVIES_PATH}\n"
            "Vui long chay 'python fetch_movies.py --pages 100' truoc."
        )

    with open(MOVIES_PATH, "r", encoding="utf-8") as f:
        movies = json.load(f)

    print(f"Dang xu ly {len(movies)} phim...")
    documents = [build_document(m) for m in movies]

    vectorizer = TfidfVectorizer(min_df=1)
    tfidf_matrix = vectorizer.fit_transform(documents)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(INDEX_PATH, "wb") as f:
        pickle.dump({
            "vectorizer": vectorizer,
            "tfidf_matrix": tfidf_matrix,
            "movies": movies,
        }, f)

    print(f"Da xay xong index: {tfidf_matrix.shape[0]} van ban, {tfidf_matrix.shape[1]} tu vung")
    print(f"Luu vao {INDEX_PATH}")



if __name__ == "__main__":
    main()
