import sqlite3

conn = sqlite3.connect("words.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hungarian_word TEXT NOT NULL,
    english_meaning TEXT NOT NULL,
    hungarian_sentence TEXT,
    english_sentence TEXT,
    suffixes TEXT,
    duolingo_unit TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
