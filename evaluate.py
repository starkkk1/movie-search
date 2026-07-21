"""
Module 5 - Danh gia he thong

Sua QUERIES ben duoi: voi moi truy van, dien "relevant" la danh sach ID phim
ban tu xac dinh la dung (ground truth). Lay ID bang cach chay:
    python search.py "<query>"
roi mo data/movies.json de tim id cua nhung phim ban thay phu hop, hoac in
them id trong search.py.

Chay: python evaluate.py
"""
from search import search

# TODO: thay bang 10-20 truy van that va id ground truth cua ban.
# Vi du minh hoa (id la id lay tu TMDB, ban can dien id thuc te sau khi
# chay python search.py "<query>" va xem ket qua):
QUERIES = [
    {"query": "phim hanh dong", "relevant": []},
    {"query": "phim kinh di", "relevant": []},
    {"query": "phim hoat hinh gia dinh", "relevant": []},
    # ... them cac truy van con lai
]


def precision_at_k(results: list, relevant: set, k: int = 10) -> float:
    top_k = results[:k]
    if not top_k:
        return 0.0
    hits = sum(1 for r in top_k if r["id"] in relevant)
    return hits / len(top_k)


def average_precision(results: list, relevant: set) -> float:
    if not relevant:
        return 0.0
    hits = 0
    precisions = []
    for i, r in enumerate(results, start=1):
        if r["id"] in relevant:
            hits += 1
            precisions.append(hits / i)
    if not precisions:
        return 0.0
    return sum(precisions) / len(relevant)


def main():
    p_scores, ap_scores = [], []
    for item in QUERIES:
        relevant = set(item["relevant"])
        results = search(item["query"], top_k=10)
        p = precision_at_k(results, relevant, k=10)
        ap = average_precision(results, relevant)
        p_scores.append(p)
        ap_scores.append(ap)
        print(f"'{item['query']}': Precision@10={p:.3f}  AP={ap:.3f}")

    if p_scores:
        print(f"\nMean Precision@10: {sum(p_scores)/len(p_scores):.3f}")
        print(f"MAP: {sum(ap_scores)/len(ap_scores):.3f}")


if __name__ == "__main__":
    main()
