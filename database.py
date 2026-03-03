import sqlite3
import os
import bcrypt
from datetime import datetime

DB_PATH = "pagevault.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs("books", exist_ok=True)
    os.makedirs("covers", exist_ok=True)
    
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        joined_at TEXT DEFAULT CURRENT_TIMESTAMP,
        last_login TEXT
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT NOT NULL,
        description TEXT,
        cover_path TEXT,
        file_path TEXT,
        uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
        uploaded_by INTEGER
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS ratings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        stars INTEGER NOT NULL,
        review_text TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, book_id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_title TEXT NOT NULL,
        author TEXT,
        reason TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS wishlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        UNIQUE(user_id, book_id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS reading_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        read_at TEXT DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, book_id)
    )''')
    
    # Create admin user if not exists
    admin_email = "admin@pagevault.com"
    existing = c.execute("SELECT id FROM users WHERE email=?", (admin_email,)).fetchone()
    if not existing:
        pw_hash = bcrypt.hashpw("pagevault2024".encode(), bcrypt.gensalt()).decode()
        c.execute('''INSERT INTO users (name, email, password_hash, role, joined_at)
                     VALUES (?, ?, ?, 'admin', ?)''',
                  ("Admin", admin_email, pw_hash, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

# ── AUTH ──────────────────────────────────────────────────────────────────────

def register_user(name, email, password):
    conn = get_connection()
    c = conn.cursor()
    if c.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone():
        conn.close()
        return False, "Email already registered."
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    c.execute('''INSERT INTO users (name, email, password_hash, role, joined_at)
                 VALUES (?, ?, ?, 'user', ?)''',
              (name, email, pw_hash, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    return True, "Registered successfully!"

def login_user(email, password):
    conn = get_connection()
    c = conn.cursor()
    # Allow admin login by username 'admin'
    if email.lower() == "admin":
        row = c.execute("SELECT * FROM users WHERE role='admin'").fetchone()
    else:
        row = c.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()
    if row and bcrypt.checkpw(password.encode(), row["password_hash"].encode()):
        c.execute("UPDATE users SET last_login=? WHERE id=?",
                  (datetime.now().isoformat(), row["id"]))
        conn.commit()
        conn.close()
        return True, dict(row)
    conn.close()
    return False, "Invalid credentials."

# ── BOOKS ─────────────────────────────────────────────────────────────────────

def add_book(title, author, genre, description, cover_path, file_path, uploaded_by):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO books (title, author, genre, description, cover_path, file_path, uploaded_at, uploaded_by)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (title, author, genre, description, cover_path, file_path,
               datetime.now().isoformat(), uploaded_by))
    conn.commit()
    conn.close()

def get_all_books(genre=None, search=None):
    conn = get_connection()
    c = conn.cursor()
    query = "SELECT * FROM books WHERE 1=1"
    params = []
    if genre and genre != "All":
        query += " AND genre=?"
        params.append(genre)
    if search:
        query += " AND (title LIKE ? OR author LIKE ?)"
        params += [f"%{search}%", f"%{search}%"]
    query += " ORDER BY uploaded_at DESC"
    rows = c.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_book(book_id):
    conn = get_connection()
    c = conn.cursor()
    row = c.execute("SELECT * FROM books WHERE id=?", (book_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def delete_book(book_id):
    conn = get_connection()
    c = conn.cursor()
    book = c.execute("SELECT * FROM books WHERE id=?", (book_id,)).fetchone()
    if book:
        for path in [book["cover_path"], book["file_path"]]:
            if path and os.path.exists(path):
                os.remove(path)
        c.execute("DELETE FROM books WHERE id=?", (book_id,))
        c.execute("DELETE FROM ratings WHERE book_id=?", (book_id,))
        c.execute("DELETE FROM wishlist WHERE book_id=?", (book_id,))
        c.execute("DELETE FROM reading_history WHERE book_id=?", (book_id,))
        conn.commit()
    conn.close()

def get_featured_books(limit=6):
    conn = get_connection()
    c = conn.cursor()
    rows = c.execute('''SELECT b.*, AVG(r.stars) as avg_rating
                        FROM books b LEFT JOIN ratings r ON b.id=r.book_id
                        GROUP BY b.id ORDER BY avg_rating DESC NULLS LAST LIMIT ?''', (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ── RATINGS ───────────────────────────────────────────────────────────────────

def upsert_rating(user_id, book_id, stars, review_text):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO ratings (user_id, book_id, stars, review_text, created_at)
                 VALUES (?, ?, ?, ?, ?)
                 ON CONFLICT(user_id, book_id) DO UPDATE SET
                 stars=excluded.stars, review_text=excluded.review_text, created_at=excluded.created_at''',
              (user_id, book_id, stars, review_text, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_book_ratings(book_id):
    conn = get_connection()
    c = conn.cursor()
    rows = c.execute('''SELECT r.*, u.name as user_name
                        FROM ratings r JOIN users u ON r.user_id=u.id
                        WHERE r.book_id=? ORDER BY r.created_at DESC''', (book_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_avg_rating(book_id):
    conn = get_connection()
    c = conn.cursor()
    row = c.execute("SELECT AVG(stars) as avg, COUNT(*) as cnt FROM ratings WHERE book_id=?", (book_id,)).fetchone()
    conn.close()
    return row["avg"] or 0, row["cnt"]

def get_user_rating(user_id, book_id):
    conn = get_connection()
    c = conn.cursor()
    row = c.execute("SELECT * FROM ratings WHERE user_id=? AND book_id=?", (user_id, book_id)).fetchone()
    conn.close()
    return dict(row) if row else None

# ── REQUESTS ──────────────────────────────────────────────────────────────────

def submit_request(user_id, book_title, author, reason):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT INTO requests (user_id, book_title, author, reason, status, created_at)
                 VALUES (?, ?, ?, ?, 'pending', ?)''',
              (user_id, book_title, author, reason, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_all_requests():
    conn = get_connection()
    c = conn.cursor()
    rows = c.execute('''SELECT req.*, u.name as user_name, u.email as user_email
                        FROM requests req JOIN users u ON req.user_id=u.id
                        ORDER BY req.created_at DESC''').fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_user_requests(user_id):
    conn = get_connection()
    c = conn.cursor()
    rows = c.execute("SELECT * FROM requests WHERE user_id=? ORDER BY created_at DESC", (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_request_status(req_id, status):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE requests SET status=? WHERE id=?", (status, req_id))
    conn.commit()
    conn.close()

# ── WISHLIST ──────────────────────────────────────────────────────────────────

def toggle_wishlist(user_id, book_id):
    conn = get_connection()
    c = conn.cursor()
    existing = c.execute("SELECT id FROM wishlist WHERE user_id=? AND book_id=?", (user_id, book_id)).fetchone()
    if existing:
        c.execute("DELETE FROM wishlist WHERE user_id=? AND book_id=?", (user_id, book_id))
        result = False
    else:
        c.execute("INSERT INTO wishlist (user_id, book_id) VALUES (?, ?)", (user_id, book_id))
        result = True
    conn.commit()
    conn.close()
    return result

def get_user_wishlist(user_id):
    conn = get_connection()
    c = conn.cursor()
    rows = c.execute('''SELECT b.* FROM books b
                        JOIN wishlist w ON b.id=w.book_id
                        WHERE w.user_id=? ORDER BY w.id DESC''', (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def is_in_wishlist(user_id, book_id):
    conn = get_connection()
    c = conn.cursor()
    row = c.execute("SELECT id FROM wishlist WHERE user_id=? AND book_id=?", (user_id, book_id)).fetchone()
    conn.close()
    return row is not None

# ── READING HISTORY ───────────────────────────────────────────────────────────

def mark_as_read(user_id, book_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute('''INSERT OR IGNORE INTO reading_history (user_id, book_id, read_at)
                 VALUES (?, ?, ?)''', (user_id, book_id, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_reading_history(user_id):
    conn = get_connection()
    c = conn.cursor()
    rows = c.execute('''SELECT b.*, rh.read_at FROM books b
                        JOIN reading_history rh ON b.id=rh.book_id
                        WHERE rh.user_id=? ORDER BY rh.read_at DESC''', (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_books_read_count(user_id):
    conn = get_connection()
    c = conn.cursor()
    row = c.execute("SELECT COUNT(*) as cnt FROM reading_history WHERE user_id=?", (user_id,)).fetchone()
    conn.close()
    return row["cnt"]

# ── ADMIN ─────────────────────────────────────────────────────────────────────

def get_all_users():
    conn = get_connection()
    c = conn.cursor()
    rows = c.execute("SELECT * FROM users ORDER BY joined_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_stats():
    conn = get_connection()
    c = conn.cursor()
    stats = {}
    stats["total_books"] = c.execute("SELECT COUNT(*) as cnt FROM books").fetchone()["cnt"]
    stats["total_users"] = c.execute("SELECT COUNT(*) as cnt FROM users WHERE role='user'").fetchone()["cnt"]
    stats["total_reviews"] = c.execute("SELECT COUNT(*) as cnt FROM ratings").fetchone()["cnt"]
    stats["pending_requests"] = c.execute("SELECT COUNT(*) as cnt FROM requests WHERE status='pending'").fetchone()["cnt"]
    top = c.execute('''SELECT b.title, AVG(r.stars) as avg, COUNT(r.id) as cnt
                       FROM books b JOIN ratings r ON b.id=r.book_id
                       GROUP BY b.id ORDER BY avg DESC LIMIT 5''').fetchall()
    stats["top_books"] = [dict(t) for t in top]
    conn.close()
    return stats