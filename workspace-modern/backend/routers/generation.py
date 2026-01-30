"""
Generation Router - API Endpoints for Document Generation
Handles PDF and Word export functionality
"""
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import io
import os
from datetime import datetime

# Import generators (we will implement these next)
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False

try:
    from docx import Document
    from docx.shared import Pt, Inches
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

from utils.template_generator import generate_html_template

router = APIRouter(prefix="/api/generate", tags=["generation"])

class GenerateRequest(BaseModel):
    title: str
    type: str
    data: Dict[str, Any]
    color_scheme: Optional[str] = 'azul-tesla'
    font: Optional[str] = 'Calibri'

@router.post("/pdf")
async def generate_pdf(request: GenerateRequest):
    """Generate PDF document from data"""
    if not WEASYPRINT_AVAILABLE:
        raise HTTPException(
            status_code=500, 
            detail="PDF generation library (WeasyPrint) not installed"
        )
        
    try:
        # 1. Generate HTML content
        html_content = generate_html_template(
            request.type, 
            request.data, 
            request.color_scheme,
            request.font
        )
        
        # 2. Convert to PDF
        pdf_file = io.BytesIO()
        HTML(string=html_content).write_pdf(pdf_file)
        pdf_file.seek(0)
        
        # 3. Return as downloadable file
        filename = f"{request.title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
        
        return Response(
            content=pdf_file.getvalue(), 
            headers=headers, 
            media_type="application/pdf"
        )
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating PDF: {str(e)}")

@router.post("/word")
async def generate_word(request: GenerateRequest):
    """Generate Word document from data"""
    if not DOCX_AVAILABLE:
        raise HTTPException(
            status_code=500, 
            detail="Word generation library (python-docx) not installed"
        )
        
    try:
        # Create Word document
        doc = Document()
        
        # Add basic content (simplified for now, mimicking structure)
        doc.add_heading(request.title, 0)
        
        p = doc.add_paragraph()
        p.add_run(f"Tipo: {request.type}\n").bold = True
        p.add_run(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}\n")
        
        # Add data dump for now (robust logic would go in a utility)
        doc.add_heading('Datos del Documento', level=1)
        
        # Client info
        if 'cliente' in request.data:
            doc.add_heading('Cliente', level=2)
            for key, value in request.data['cliente'].items():
                doc.add_paragraph(f"{key.capitalize()}: {value}")
                
        # Project info
        if 'proyecto' in request.data:
            doc.add_heading('Proyecto', level=2)
            for key, value in request.data['proyecto'].items():
                doc.add_paragraph(f"{key.capitalize()}: {value}")
        
        # Save to buffer
        docx_file = io.BytesIO()
        doc.save(docx_file)
        docx_file.seek(0)
        
        filename = f"{request.title.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.docx"
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
        
        return Response(
            content=docx_file.getvalue(),
            headers=headers,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

    except Exception as e:
        print(f"Error generating Word: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating Word doc: {str(e)}")
