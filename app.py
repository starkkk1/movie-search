"""
Module 4 - Giao dien Web (Flask)

Routes:
    GET /              Trang chu: o nhap tim kiem
    GET /search        Trang ket qua: hien thi, highlight, phan trang
    GET /api/search    JSON API (cho frontend Next.js)

Chay: python app.py
Mo trinh duyet: http://127.0.0.1:5000
"""
import re
import math

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from markupsafe import Markup, escape

from search import search as do_search

app = Flask(__name__)
CORS(app)

RESULTS_PER_PAGE = 10
TMDB_MOVIE_URL   = "https://www.themoviedb.org/movie/{id}"
TMDB_POSTER_BASE = "https://image.tmdb.org/t/p/w185"


# ── Helpers ──────────────────────────────────────────────────

def highlight(text: str, query: str) -> Markup:
    """Wrap query tokens trong <mark> de highlight trong doan tom tat."""
    if not text or not query:
        return Markup(escape(text or ""))
    tokens = [re.escape(t) for t in query.split() if len(t) > 1]
    if not tokens:
        return Markup(escape(text))
    pattern = re.compile(r"(" + "|".join(tokens) + r")", re.IGNORECASE)
    result = pattern.sub(r"<mark>\1</mark>", escape(text))
    return Markup(result)


def paginate(items: list, page: int, per_page: int) -> dict:
    total      = len(items)
    total_pages = max(1, math.ceil(total / per_page))
    page        = max(1, min(page, total_pages))
    start       = (page - 1) * per_page
    return {
        "items":       items[start : start + per_page],
        "page":        page,
        "total":       total,
        "total_pages": total_pages,
        "has_prev":    page > 1,
        "has_next":    page < total_pages,
    }


# ── Routes ───────────────────────────────────────────────────

@app.route("/")
def home():
    """Trang chu: chi co o tim kiem."""
    return render_template("home.html")


@app.route("/search")
def search():
    """Trang ket qua: phan trang + highlight."""
    query    = request.args.get("q", "").strip()
    page     = int(request.args.get("page", 1))

    if not query:
        return redirect(url_for("home"))

    all_results = do_search(query, top_k=100)   # lay nhieu de phan trang

    # Them link TMDB va highlight
    for r in all_results:
        r["tmdb_url"]   = TMDB_MOVIE_URL.format(id=r["id"])
        r["poster_url"] = (TMDB_POSTER_BASE + r["poster_path"]) if r.get("poster_path") else None
        r["overview_hl"] = highlight(r.get("overview", ""), query)

    paged = paginate(all_results, page, RESULTS_PER_PAGE)

    return render_template(
        "results.html",
        query   = query,
        results = paged["items"],
        page    = paged["page"],
        total   = paged["total"],
        total_pages = paged["total_pages"],
        has_prev    = paged["has_prev"],
        has_next    = paged["has_next"],
    )


@app.route("/api/search")
def api_search():
    """JSON API (giu nguyen cho Next.js frontend)."""
    query   = request.args.get("q", "").strip()
    results = do_search(query, top_k=20) if query else []
    return jsonify({"query": query, "results": results})


if __name__ == "__main__":
    app.run(debug=True)
