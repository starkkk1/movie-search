"""
Module 1 - Thu thap du lieu (Crawling)
Tai du lieu phim tu TMDB API va luu ra data/movies.json

Cach dung:
    1. Dang ky tai khoan mien phi tai https://www.themoviedb.org/
    2. Vao Settings -> API -> lay "API Read Access Token" (v4 auth, dang chuoi dai bat dau bang "eyJ...")
    3. Chay: python fetch_movies.py --token YOUR_TOKEN --pages 100
       (moi page ~20 phim, 100 page ~ 2000 phim, du de demo)
"""
import argparse
import json
import time

import requests

BASE_URL = "https://api.themoviedb.org/3"
GENRE_URL = f"{BASE_URL}/genre/movie/list?language=vi"
DISCOVER_URL = f"{BASE_URL}/discover/movie?language=vi&sort_by=popularity.desc&page={{page}}"

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


def fetch_movies(token: str, pages: int) -> list:
    genre_map = fetch_genres(token)
    movies = []
    for page in range(1, pages + 1):
        url = DISCOVER_URL.format(page=page)
        try:
            data = call_api(url, token)
        except Exception as e:
            print(f"  page {page} loi sau {MAX_RETRIES} lan thu: {e}, bo qua page nay")
            continue

        for m in data.get("results", []):
            movies.append({
                "id": m.get("id"),
                "title": m.get("title", ""),
                "original_title": m.get("original_title", ""),
                "overview": m.get("overview", ""),
                "genres": [genre_map.get(gid, "") for gid in m.get("genre_ids", [])],
                "release_date": m.get("release_date", ""),
                "vote_average": m.get("vote_average", 0),
                "poster_path": m.get("poster_path", ""),
            })

        print(f"  page {page}/{pages} xong, tong {len(movies)} phim")
        time.sleep(0.25)  # tranh vuot rate limit

    return movies


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", required=True, help="TMDB API Read Access Token")
    parser.add_argument("--pages", type=int, default=100, help="So trang can tai (moi trang ~20 phim)")
    parser.add_argument("--out", default="data/movies.json")
    args = parser.parse_args()

    print(f"Bat dau tai du lieu ({args.pages} trang)...")
    movies = fetch_movies(args.token, args.pages)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)

    print(f"Da luu {len(movies)} phim vao {args.out}")


if __name__ == "__main__":
    main()
