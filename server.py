#!/usr/bin/env python3
"""
yt-key-test-v1: Mini Flask app để test redirect YouTube bằng key
"""

from flask import Flask, redirect

app = Flask(__name__)

# Trang chủ để check server có chạy không
@app.route("/")
def home():
    return "✅ Server chạy OK - nhập key vào URL để test."

# Route động nhận key
@app.route("/<key>")
def open_key(key):
    # Ví dụ: preyoutube-0388486866-2709-vf6p
    if key.lower().startswith("preyoutube"):
        # TODO: Ở đây bạn có thể map key → link riêng
        # Tạm thời redirect chung sang YouTube
        return redirect("https://www.youtube.com")
    return "❌ Key không hợp lệ!"

if __name__ == "__main__":
    # Render sẽ tự động chọn cổng qua biến môi trường, nhưng khi chạy local thì mặc định port 5000
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
