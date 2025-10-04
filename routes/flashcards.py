from fastapi import APIRouter
import sqlite3

router = APIRouter()

@router.get("/words")
def get_words(unit: str = None):
    conn = sqlite3.connect("words.db")
    cursor = conn.cursor()
    if unit:
        cursor.execute("SELECT * FROM words WHERE duolingo_unit = ?", (unit,))
    else:
        cursor.execute("SELECT * FROM words")
    rows = cursor.fetchall()
    conn.close()
    return [
        dict(zip([
            "id", "hungarian_word", "english_meaning",
            "hungarian_sentence", "english_sentence",
            "suffixes", "duolingo_unit", "created_at"
        ], row)) for row in rows
    ]
