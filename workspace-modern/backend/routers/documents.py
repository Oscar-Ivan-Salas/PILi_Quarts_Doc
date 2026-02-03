"""
Document Router - API Endpoints for Document Management
Handles CRUD operations for all document types using SQLite
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import json

from database.sqlite_config import get_db
from database.models_sqlite import Document, Project, Quote

router = APIRouter(prefix="/api/documents", tags=["documents"])

# --- Schemas ---

class DocumentBase(BaseModel):
    title: str
    type: str  # proyecto-simple, cotizacion-simple, etc.
    data: dict
    color_scheme: Optional[str] = 'azul-tesla'
    font: Optional[str] = 'Calibri'
    user_id: str

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# --- Endpoints ---

@router.post("/", response_model=DocumentResponse)
def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    """Create a new document"""
    db_doc = Document(
        title=doc.title,
        type=doc.type,
        data=doc.data,  # SQLAlchemy handles JSON automatically
        color_scheme=doc.color_scheme,
        font=doc.font,
        user_id=doc.user_id
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@router.get("/", response_model=List[DocumentResponse])
def get_documents(user_id: str, type: Optional[str] = None, db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    """Get all documents for a user, optionally filtered by type"""
    query = db.query(Document).filter(Document.user_id == user_id)
    if type:
        query = query.filter(Document.type.contains(type))
    return query.offset(skip).limit(limit).all()

@router.get("/{doc_id}", response_model=DocumentResponse)
def get_document(doc_id: int, db: Session = Depends(get_db)):
    """Get a specific document by ID"""
    db_doc = db.query(Document).filter(Document.id == doc_id).first()
    if db_doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_doc

@router.put("/{doc_id}", response_model=DocumentResponse)
def update_document(doc_id: int, doc: DocumentUpdate, db: Session = Depends(get_db)):
    """Update a document"""
    db_doc = db.query(Document).filter(Document.id == doc_id).first()
    if db_doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    
    db_doc.title = doc.title
    db_doc.type = doc.type
    db_doc.data = doc.data
    db_doc.color_scheme = doc.color_scheme
    db_doc.font = doc.font
    
    db.commit()
    db.refresh(db_doc)
    return db_doc

@router.delete("/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    """Delete a document"""
    db_doc = db.query(Document).filter(Document.id == doc_id).first()
    if db_doc is None:
        raise HTTPException(status_code=404, detail="Document not found")
    
    db.delete(db_doc)
    db.commit()
    return {"message": "Document deleted successfully"}
