from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
import sqlite3

router = APIRouter()

# 🧭 View all words
@router.get("/admin", response_class=HTMLResponse)
def admin_dashboard():
    conn = sqlite3.connect("static/words.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM words")
    rows = cursor.fetchall()
    conn.close()

    html = "<h2>Hungarian Flashcards Admin</h2><table border='1'>"
    html += "<tr><th>ID</th><th>Hungarian</th><th>English</th><th>Unit</th><th>Actions</th></tr>"
    for row in rows:
        html += f"""
        <tr>
            <td>{row[0]}</td>
            <td>{row[1]}</td>
            <td>{row[2]}</td>
            <td>{row[6]}</td>
            <td>
                <a href='/admin/edit/{row[0]}'>Edit</a> |
                <a href='/admin/delete/{row[0]}'>Delete</a>
            </td>
        </tr>
        """
    html += "</table><br><a href='/admin/add-form'>Add New Word</a>"
    html += "<br><br><a href='/static/words.db' download>📥 Download words.db</a>"
    return html

# ➕ Add form
@router.get("/admin/add-form", response_class=HTMLResponse)
def add_form():
    return """
    <h2>Add New Word</h2>
    <form action="/admin/add" method="post">
        Hungarian Word: <input name="hungarian_word"><br>
        English Meaning: <input name="english_meaning"><br>
        Hungarian Sentence: <input name="hungarian_sentence"><br>
        English Sentence: <input name="english_sentence"><br>
        Suffixes: <input name="suffixes"><br>
        Duolingo Unit: <input name="duolingo_unit"><br>
        <input type="submit" value="Add">
    </form>
    """

# ➕ Add POST
@router.post("/admin/add")
def add_word(
    hungarian_word: str = Form(...),
    english_meaning: str = Form(...),
    hungarian_sentence: str = Form(""),
    english_sentence: str = Form(""),
    suffixes: str = Form(""),
    duolingo_unit: str = Form("")
):
    conn = sqlite3.connect("static/words.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO words (
            hungarian_word, english_meaning,
            hungarian_sentence, english_sentence,
            suffixes, duolingo_unit
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        hungarian_word, english_meaning,
        hungarian_sentence, english_sentence,
        suffixes, duolingo_unit
    ))
    conn.commit()
    conn.close()
    return HTMLResponse("<p>✅ Word added. <a href='/admin'>Back to admin</a></p>")

# ✏️ Edit form
@router.get("/admin/edit/{word_id}", response_class=HTMLResponse)
def edit_form(word_id: int):
    conn = sqlite3.connect("static/words.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM words WHERE id = ?", (word_id,))
    word = cursor.fetchone()
    conn.close()

    return f"""
    <h2>Edit Word</h2>
    <form action="/admin/update/{word_id}" method="post">
        Hungarian Word: <input name="hungarian_word" value="{word[1]}"><br>
        English Meaning: <input name="english_meaning" value="{word[2]}"><br>
        Hungarian Sentence: <input name="hungarian_sentence" value="{word[3]}"><br>
        English Sentence: <input name="english_sentence" value="{word[4]}"><br>
        Suffixes: <input name="suffixes" value="{word[5]}"><br>
        Duolingo Unit: <input name="duolingo_unit" value="{word[6]}"><br>
        <input type="submit" value="Update">
    </form>
    """

# ✏️ Update POST
@router.post("/admin/update/{word_id}")
def update_word(
    word_id: int,
    hungarian_word: str = Form(...),
    english_meaning: str = Form(...),
    hungarian_sentence: str = Form(""),
    english_sentence: str = Form(""),
    suffixes: str = Form(""),
    duolingo_unit: str = Form("")
):
    conn = sqlite3.connect("static/words.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE words SET
        hungarian_word = ?, english_meaning = ?,
        hungarian_sentence = ?, english_sentence = ?,
        suffixes = ?, duolingo_unit = ?
        WHERE id = ?
    """, (
        hungarian_word, english_meaning,
        hungarian_sentence, english_sentence,
        suffixes, duolingo_unit, word_id
    ))
    conn.commit()
    conn.close()
    return HTMLResponse("<p>✅ Word updated. <a href='/admin'>Back to admin</a></p>")

# ❌ Delete
@router.get("/admin/delete/{word_id}", response_class=HTMLResponse)
def delete_word(word_id: int):
    conn = sqlite3.connect("static/words.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM words WHERE id = ?", (word_id,))
    conn.commit()
    conn.close()
    return HTMLResponse("<p>🗑️ Word deleted. <a href='/admin'>Back to admin</a></p>")
