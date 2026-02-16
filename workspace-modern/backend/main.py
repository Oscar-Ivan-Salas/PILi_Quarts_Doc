"""
Main Application Entry Point - Updates
Includes new SQLite database initialization and document router
"""
# Force reload - Checkpoint 10471
from fastapi import FastAPI, Request
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
origins = [
    "http://localhost:3010",
    "http://localhost:5173",
    "http://127.0.0.1:3010",
    "http://localhost:3011",
    "http://127.0.0.1:3011",
    "http://localhost:8000",
    "http://localhost:3030", # Self-reference
    "http://127.0.0.1:3030",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(documents.router)
app.include_router(generation.router)

from modules.pili.api import router as pili_router
app.include_router(pili_router.router)
# Include v2 Router for Document Generation
from modules.pili.api.router import router as pili_v2_router
app.include_router(pili_v2_router)

# Mount Static Files (for avatars, logos, generated PDFs)
static_path = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_path):
    os.makedirs(static_path)
app.mount("/static", StaticFiles(directory=static_path), name="static")

@app.get("/")
def read_root():
    return {"status": "online", "message": "PILi Quarts API is running"}

# Initialize Socket Manager
import socketio
from modules.pili.api.router import get_pili_brain

# Create Socket.IO Server
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
# Wrap FastAPI app with Socket.IO ASGI app
# Critical: Reassign 'app' so uvicorn main:app runs the wrapper!
app = socketio.ASGIApp(sio, app)

# Helper to get brain (since we are outside of request context)
def get_brain_instance():
    return get_pili_brain()

# Verify Socket Connection
@sio.event
async def connect(sid, environ, auth=None):
    print(f"Socket Connected: {sid}")
    # Initialize session
    await sio.save_session(sid, {'user_id': str(sid)})
    
    # Welcome message
    await sio.emit('message', {
        "type": "connected",
        "message": "¡Hola! Soy PILI, tu asistente de ingeniería. ¿En qué puedo ayudarte?",
        "timestamp": "now" # TODO: Real timestamp
    }, to=sid)

@sio.event
async def disconnect(sid):
    print(f"Socket Disconnected: {sid}")

@sio.event
async def message(sid, data):
    try:
        # data = {'message': '...', 'context': {...}}
        print(f"Message from {sid}: {data}")
        
        user_msg = data.get('message', '')
        context = data.get('context', {})
        
        # Get Brain
        brain = get_brain_instance()
        
        # Send Typing
        await sio.emit('typing', True, to=sid)
        
        # Process (Mocking User ID as SID for now since we don't have auth yet)
        result = await brain.process_message(
            user_id=str(sid),
            message=user_msg,
            context=context
        )
        
        await sio.emit('typing', False, to=sid)
        
        # Send Response
        await sio.emit('message', {
            "type": "message",
            "response": result["response"],
            "extracted_data": result.get("extracted_data"),
            "suggestions": result.get("suggestions", []),
            "timestamp": result["timestamp"]
        }, to=sid)

    except Exception as e:
        print(f"Error processing message: {e}")
        await sio.emit('message', {
            "type": "error",
            "content": f"Error: {str(e)}",
            "timestamp": "now"
        }, to=sid)
