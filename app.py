"""
Module 4 - Giao dien Web

Chay: python app.py
Mo trinh duyet: http://127.0.0.1:5000
"""
from flask import Flask, render_template, request

from search import search

app = Flask(__name__)


@app.route("/")
def home():
    query = request.args.get("q", "").strip()
    results = search(query, top_k=20) if query else []
    return render_template("index.html", query=query, results=results)


if __name__ == "__main__":
    app.run(debug=True)
