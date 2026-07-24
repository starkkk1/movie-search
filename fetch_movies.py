"""
Module 1 - Thu thap du lieu (Crawling)
Tai du lieu phim tu TMDB API va luu ra data/movies.json

Cach dung:
    1. Dang ky tai khoan mien phi tai https://www.themoviedb.org/
    2. Vao Settings -> API -> lay "API Read Access Token" (v4 auth, chuoi bat dau bang "eyJ...")
    3. Sao chep .env.example thanh .env, dien token vao TMDB_TOKEN
    4. Chay: python fetch_movies.py --pages 100
       (moi page ~20 phim, 100 page ~ 2000 phim; chi giu phim tieng Viet va tieng Anh)
"""
import argparse
import json
import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()  # Doc bien moi truong tu file .env (neu co)

BASE_URL = "https://api.themoviedb.org/3"
GENRE_URL = f"{BASE_URL}/genre/movie/list?language=vi"
DISCOVER_URL = BASE_URL + "/discover/movie?language=vi&sort_by=popularity.desc&page={page}"

ALLOWED_LANGUAGES = {"vi", "en"}  # Chi lay phim tieng Viet va tieng Anh
MAX_RETRIES = 4


def call_api(url: str, token: str) -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json",
        # Mot so mang/firewall chan request khong co User-Agent giong trinh duyet
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    }
    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout,
                requests.exceptions.HTTPError) as e:
            last_error = e
            wait = attempt * 2
            print(f"    (lan {attempt}/{MAX_RETRIES} that bai: {e}, thu lai sau {wait}s)")
            time.sleep(wait)
    raise last_error


def fetch_genres(token: str) -> dict:
    data = call_api(GENRE_URL, token)
    return {g["id"]: g["name"] for g in data.get("genres", [])}


def fetch_movies(token: str, pages: int, allowed_languages: set = None) -> list:
    if allowed_languages is None:
        allowed_languages = ALLOWED_LANGUAGES
    genre_map = fetch_genres(token)
    movies = []
    skipped = 0
    for page in range(1, pages + 1):
        url = DISCOVER_URL.format(page=page)
        try:
            data = call_api(url, token)
        except Exception as e:
            print(f"  page {page} loi sau {MAX_RETRIES} lan thu: {e}, bo qua page nay")
            continue

        for m in data.get("results", []):
            lang = m.get("original_language", "")
            if lang not in allowed_languages:
                skipped += 1
                continue
            movies.append({
                "id": m.get("id"),
                "title": m.get("title", ""),
                "original_title": m.get("original_title", ""),
                "original_language": lang,
                "overview": m.get("overview", ""),
                "genres": [genre_map.get(gid, "") for gid in m.get("genre_ids", [])],
                "release_date": m.get("release_date", ""),
                "vote_average": m.get("vote_average", 0),
                "poster_path": m.get("poster_path", ""),
            })

        print(f"  page {page}/{pages} xong, tong {len(movies)} phim (bo qua {skipped} phim ngon ngu khac)")
        time.sleep(0.25)  # tranh vuot rate limit

    print(f"\nHoan thanh: {len(movies)} phim hop le, bo qua {skipped} phim ngon ngu khac.")
    return movies


from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_OUT = BASE_DIR / "data" / "movies.json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--token",
        default=None,
        help="TMDB API Read Access Token (neu khong truyen, doc tu bien moi truong TMDB_TOKEN trong .env)",
    )
    parser.add_argument("--pages", type=int, default=100, help="So trang can tai (moi trang ~20 phim)")
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    parser.add_argument(
        "--languages",
        default="vi,en",
        help="Danh sach ngon ngu cho phep, cach nhau bang dau phay (mac dinh: vi,en)",
    )
    args = parser.parse_args()

    token = args.token or os.getenv("TMDB_TOKEN")
    if not token:
        parser.error(
            "Can cung cap token: dung --token hoac dat TMDB_TOKEN=... trong file .env"
        )

    allowed = set(args.languages.split(","))
    print(f"Bat dau tai du lieu ({args.pages} trang), chi lay ngon ngu: {allowed}...")
    movies = fetch_movies(token, args.pages, allowed_languages=allowed)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)

    print(f"Da luu {len(movies)} phim vao {out_path}")



if __name__ == "__main__":
    main()
