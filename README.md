# Máy Tìm Kiếm Phim (Vertical Search Engine)

Đồ án cuối kỳ — máy tìm kiếm chuyên sâu cho lĩnh vực phim ảnh.

## Cài đặt

```bash
pip install -r requirements.txt
```

## Chạy theo thứ tự

### 1. Lấy TMDB API token (miễn phí)
- Đăng ký tại https://www.themoviedb.org/
- Vào **Settings → API → API Read Access Token (v4 auth)**
- Copy chuỗi token (bắt đầu bằng `eyJ...`)

### 2. Tải dữ liệu phim (Module 1)
```bash
python fetch_movies.py --token YOUR_TOKEN --pages 100
```
`--pages 100` ≈ 2000 phim, đủ để demo. Tăng lên nếu muốn nhiều dữ liệu hơn (nhưng sẽ lâu hơn).

### 3. Xây chỉ mục TF-IDF (Module 2 + 3)
```bash
python build_index.py
```

### 4. Thử tìm kiếm bằng dòng lệnh (tùy chọn, để kiểm tra nhanh)
```bash
python search.py "phim hành động siêu anh hùng"
```

### 5. Chạy giao diện web (Module 4)
```bash
python app.py
```
Mở trình duyệt: http://127.0.0.1:5000

### 6. Đánh giá hệ thống (Module 5)
- Mở `evaluate.py`, điền 10–20 truy vấn thật vào `QUERIES` và ID phim đúng (ground truth) cho mỗi truy vấn (chạy `search.py` để xem ID trong `data/movies.json`).
- Chạy:
```bash
python evaluate.py
```
Kết quả in ra Precision@10 và MAP cho từng truy vấn + trung bình — dùng số liệu này cho báo cáo.

## Cấu trúc thư mục

```
movie_search/
├── fetch_movies.py   # Module 1: tải dữ liệu từ TMDB
├── build_index.py    # Module 2+3: làm sạch text, xây TF-IDF index
├── search.py          # Module 3: tìm kiếm + xếp hạng (cosine similarity)
├── app.py              # Module 4: giao diện web Flask
├── evaluate.py        # Module 5: tính Precision@10, MAP
├── templates/
│   └── index.html     # giao diện trang tìm kiếm
├── data/
│   ├── movies.json    # dữ liệu thô (sinh ra sau bước 2)
│   └── index.pkl       # chỉ mục TF-IDF (sinh ra sau bước 3)
└── requirements.txt
```

## Ghi chú cho báo cáo

- **Thuật toán xếp hạng**: TF-IDF (scikit-learn `TfidfVectorizer`) + cosine similarity giữa vector truy vấn và vector tài liệu.
- **Trọng số theo trường**: tên phim và thể loại được lặp lại nhiều lần trong văn bản trước khi đưa vào TF-IDF, để những từ khớp tên phim/thể loại có điểm cao hơn khớp trong phần tóm tắt — cách đơn giản để đạt hiệu ứng "trọng số theo trường" mà không cần code TF-IDF thủ công.
- Có thể nâng cấp thêm: BM25 thay TF-IDF, tách gốc từ tiếng Việt bằng `underthesea`, phân trang kết quả — nếu còn thời gian sau khi bản MVP chạy ổn.
