# yt-key-test-v1

Dev sandbox để kiểm tra luồng: nhập **key** → gọi API `/api/verify` → nếu hợp lệ thì **redirect sang YouTube Mobile**.

> Chỉ dùng cho mục đích phát triển/kiểm thử. **Không** dùng để vượt/đè cơ chế an toàn của xe.

## Chạy cục bộ
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python server.py
# mở http://localhost:5000
```

## Seed key
DB SQLite (`keys.db`) sẽ tự tạo lần đầu chạy và seed sẵn 1 key:
```
preyoutube-0389667823-20250925-VF6p
```

## Deploy với Docker (local)
```bash
docker build -t yt-key-test-v1 .
docker run -p 5000:5000 yt-key-test-v1
# mở http://localhost:5000
```

## Deploy lên Render (HTTPS public)
1. Đưa 4 file này lên repo GitHub: `server.py`, `templates/index.html`, `requirements.txt`, `Dockerfile` (Dockerfile tùy chọn).
2. Render.com → New → Web Service → kết nối repo.
3. Deploy (Render sẽ cấp một URL dạng `https://<service>.onrender.com/`).

> Nếu không dùng Dockerfile: Xóa Dockerfile và dùng Start Command: `gunicorn server:app -b 0.0.0.0:$PORT`

## Sử dụng trên xe (an toàn)
- Chỉ test khi **xe đỗ (P)** hoặc do **hành khách** thao tác.
- Mở URL public (Render) trên trình duyệt của xe → nhập key → Verify → (OK) redirect YouTube.

## Thêm/đổi key
Mở Python REPL nhanh để chèn key mới:
```python
import sqlite3
conn = sqlite3.connect('keys.db')
cur = conn.cursor()
cur.execute('INSERT OR REPLACE INTO keys (key, expires_at, used) VALUES (?,?,0)',
            ('preyoutube-0123456789-20300101-VF6s', '2030-01-31'))
conn.commit(); conn.close()
```
Hoặc sửa `server.py` để seed thêm key mong muốn.
