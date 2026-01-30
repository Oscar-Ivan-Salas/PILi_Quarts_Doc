"""
Main Application Entry Point - Updates
Includes new SQLite database initialization and document router
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from database.sqlite_config import init_db
from routers import documents, generation

# Initialize FastAPI
app = FastAPI(
    title="PILi Quarts API",
    description="Backend for PILi Quarts Enterprise System",
    version="2.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database on Startup
@app.on_event("startup")
def on_startup():
    init_db()  # Creates tables if they don't exist
    print("🚀 PILi Quarts Backend Started")

# Include Routers
app.include_router(documents.router)
app.include_router(generation.router)

# Mount Static Files (for avatars, logos, generated PDFs)
static_path = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_path):
    os.makedirs(static_path)
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
def read_root():
    return {"status": "online", "message": "PILi Quarts API is running"}
