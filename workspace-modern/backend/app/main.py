from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="PILi_Quarts Workspace API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "PILi_Quarts Workspace API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "workspace-api"}
