# Máy Tìm Kiếm Phim (Vertical Search Engine)

Đồ án cuối kỳ — máy tìm kiếm chuyên sâu cho lĩnh vực phim ảnh, hỗ trợ tìm kiếm **song ngữ Việt–Anh**.

## Cài đặt

```bash
# Cài dependency Python
pip install -r requirements.txt

# Cài dependency frontend
cd frontend && npm install && cd ..
```

## Chạy theo thứ tự

### 1. Cấu hình API token

```bash
# Sao chép file mẫu
cp .env.example .env
```

Sau đó mở `.env` và điền token:
- Đăng ký miễn phí tại https://www.themoviedb.org/
- Vào **Settings → API → API Read Access Token (v4 auth)**
- Dán chuỗi token (bắt đầu bằng `eyJ...`) vào `TMDB_TOKEN`

### 2. Tải dữ liệu phim (Module 1)

```bash
python fetch_movies.py --pages 100
```

- Mỗi page ≈ 20 phim → 100 pages ≈ 1400 phim tiếng Việt/Anh.
- Phim ngôn ngữ khác (Telugu, Nhật, Trung...) tự động bị lọc bỏ khi crawl.
- Kết quả lưu ra `data/movies.json`.

### 3. Xây chỉ mục TF-IDF (Module 2 + 3)

```bash
python build_index.py
```

Lưu vectorizer và ma trận TF-IDF ra `data/index.pkl`.

### 4. Thử tìm kiếm bằng dòng lệnh *(tùy chọn)*

```bash
python search.py "phim hành động siêu anh hùng"
python search.py "horror thriller"
```

### 5. Khởi chạy ứng dụng

Cần mở **2 terminal** chạy song song:

**Terminal 1 — Backend API (Flask):**
```bash
python app.py
# Chạy tại http://127.0.0.1:5000
```

**Terminal 2 — Frontend (Next.js):**
```bash
cd frontend
npm run dev
# Chạy tại http://localhost:3000
```

Mở trình duyệt: **http://localhost:3000**

### 6. Đánh giá hệ thống (Module 5)

- Mở `evaluate.py`, điền 10–20 truy vấn thật vào `QUERIES` cùng danh sách ID phim đúng (ground truth).
- Chạy `python search.py <query>` để tra ID phim trong `data/movies.json`.
- Chạy đánh giá:

```bash
python evaluate.py
```

Kết quả in ra **Precision@10** và **MAP** cho từng truy vấn + trung bình.

## Cấu trúc thư mục

```
movie_search/
├── .env.example          # Template biến môi trường (sao chép thành .env)
├── .gitignore
├── requirements.txt
├── fetch_movies.py        # Module 1: crawl dữ liệu từ TMDB (lọc vi/en)
├── build_index.py         # Module 2+3: xử lý văn bản, xây TF-IDF index
├── search.py              # Module 3: tìm kiếm + xếp hạng (cosine similarity)
├── app.py                 # Module 4: Flask API (/, /api/search)
├── evaluate.py            # Module 5: Precision@10, MAP
├── templates/
│   └── index.html         # Giao diện Flask (legacy)
├── frontend/              # Giao diện Next.js + Tailwind CSS
│   └── src/app/
│       ├── page.tsx       # Trang chính (search + kết quả)
│       └── globals.css    # Glassmorphism, animations
└── data/                  # ← bị gitignore
    ├── movies.json        # Dữ liệu thô (sinh ra sau bước 2)
    └── index.pkl          # Chỉ mục TF-IDF (sinh ra sau bước 3)
```

## Ghi chú kỹ thuật

- **Thuật toán xếp hạng**: TF-IDF (`sklearn.TfidfVectorizer`) + cosine similarity giữa vector truy vấn và vector tài liệu.
- **Trọng số theo trường**: tên phim (`title`, `original_title`) và thể loại được lặp lại nhiều lần trước khi đưa vào TF-IDF, tạo hiệu ứng field-weighted ranking mà không cần can thiệp thủ công vào thuật toán.
- **Tìm kiếm song ngữ**: `original_title` (tiếng Anh) + bảng ánh xạ thể loại Việt–Anh được đưa vào document, cho phép tìm bằng từ khóa như "action", "horror", "sci-fi".
- **Lọc ngôn ngữ**: chỉ giữ phim có `original_language` là `vi` hoặc `en` khi crawl.
- **Frontend**: Next.js 16 + Tailwind CSS v4, giao tiếp với Flask qua proxy `/api/search`.
