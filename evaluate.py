"""
Module 5 - Danh gia he thong

Sua QUERIES ben duoi: voi moi truy van, dien "relevant" la danh sach ID phim
ban tu xac dinh la dung (ground truth). Lay ID bang cach chay:
    python search.py "<query>"
roi mo data/movies.json de tim id cua nhung phim ban thay phu hop, hoac in
them id trong search.py.

Chay: python evaluate.py
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

from search import search

# Ground truth: moi truy van kem danh sach ID phim TMDB duoc xac nhan la phu hop
QUERIES = [
    # Truy van tieng Viet - the loai
    {
        "query": "phim hành động",
        "relevant": [345887, 282035, 119450, 1236153, 1292415, 668489, 1318447, 10196],
    },
    {
        "query": "phim kinh dị",
        "relevant": [4258, 4256, 1273221, 4247, 4257, 1124620, 1138194, 1226578, 4248, 1430698],
    },
    {
        "query": "phim hoạt hình gia đình",
        "relevant": [35, 49519, 10315, 629542, 459151, 421892, 9806],
    },
    {
        "query": "phim lãng mạn tình yêu",
        "relevant": [698508, 11036, 1358005, 43347, 1097549, 19913, 43949],
    },
    {
        "query": "phim khoa học viễn tưởng",
        "relevant": [686, 34851, 1064028, 9426, 1236153, 9016, 1423191, 2675],
    },
    {
        "query": "phim tài liệu",
        "relevant": [1662317, 1715492, 1413097, 666558, 1664011, 1708739, 58395],
    },
    # Truy van tieng Anh - the loai
    {
        "query": "horror scary",
        "relevant": [1430698, 9552, 9426, 132232, 1064028, 1032823, 360784, 1477712],
    },
    {
        "query": "comedy funny",
        "relevant": [454619, 76493, 8363, 100042, 621, 1325734, 35],
    },
    {
        "query": "adventure fantasy",
        "relevant": [10196, 10195, 1698863, 763215, 9016, 639933, 10588],
    },
    # Truy van tieng Anh - ten phim cu the
    {
        "query": "Avengers",
        "relevant": [24428, 299536, 299534, 100402, 299537, 99861],
    },
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
