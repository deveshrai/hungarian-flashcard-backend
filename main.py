#import models.init_db  # This will auto-create words.db if it doesn't exist
from fastapi import FastAPI
from routes import flashcards, admin

app = FastAPI(title="Hungarian Flashcard API")

app.include_router(flashcards.router)
app.include_router(admin.router)
