import sqlite3

def get_db():
    conn = sqlite3.connect("urls.db", check_same_thread=False)
    conn.execute("CREATE TABLE IF NOT EXISTS urls (id TEXT PRIMARY KEY, url TEXT)")
    return conn

def add_url(db, short_id, url):
    db.execute("INSERT INTO urls (id, url) VALUES (?, ?)", (short_id, url))
    db.commit()

def get_url_by_short_id(db, short_id):
    cursor = db.execute("SELECT url FROM urls WHERE id=?", (short_id,))
    row = cursor.fetchone()
    return row[0] if row else None