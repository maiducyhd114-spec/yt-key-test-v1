#!/usr/bin/env python3
"""
yt-key-test-v1: dev sandbox verify key -> redirect YouTube
"""
from flask import Flask, request, jsonify, render_template
import sqlite3, os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "keys.db")
PORT = int(os.environ.get("PORT", "5000"))

app = Flask(__name__)

def init_db():
    need_seed = not os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS keys (key TEXT PRIMARY KEY, expires_at TEXT, used INTEGER DEFAULT 0)')
    if need_seed:
        # >>> KEY CỦA BẠN <<<
        cur.execute('INSERT OR IGNORE INTO keys (key, expires_at) VALUES (?, ?)',
                    ('preyoutube-0388486866-2709-VF6p', '2025-12-31'))
        conn.commit()
    conn.close()

# GỌI TRỰC TIẾP khi app khởi tạo (thay cho before_first_request)
init_db()

@app.get("/api/ping")
def ping():
    return jsonify(ok=True, service="yt-key-test-v1")

@app.post("/api/verify")
def verify():
    data = request.get_json(silent=True) or {}
    key = (data.get("key") or "").strip()
    if not key:
        return jsonify(ok=False, reason="missing_key"), 400

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    row = cur.execute('SELECT key, expires_at, used FROM keys WHERE key=?', (key,)).fetchone()
    if not row:
        conn.close()
        return jsonify(ok=False, reason="invalid_key"), 404

    expires_at, used = row[1], row[2]
    if expires_at:
        try:
            if datetime.strptime(expires_at, "%Y-%m-%d").date() < datetime.utcnow().date():
                conn.close()
                return jsonify(ok=False, reason="expired"), 403
        except Exception:
            conn.close()
            return jsonify(ok=False, reason="bad_expiry_format"), 500

    if used:
        conn.close()
        return jsonify(ok=False, reason="already_used"), 403

    cur.execute('UPDATE keys SET used=1 WHERE key=?', (key,))
    conn.commit()
    conn.close()

    return jsonify(ok=True, action="allow_feature", message="Key accepted")

@app.get("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
