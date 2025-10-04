from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import flashcards, admin
#import models.init_db  # Ensures DB is created on startup

app = FastAPI()

# Mount static folder for downloads
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include route modules
app.include_router(flashcards.router)
app.include_router(admin.router)
