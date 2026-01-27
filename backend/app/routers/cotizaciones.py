"""
Router: Cotizaciones
Endpoints para CRUD de cotizaciones Y GENERACIÓN DE DOCUMENTOS
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.core.database import get_db
from app.models.cotizacion import Cotizacion
from app.models.item import Item
from app.schemas.cotizacion import (
    CotizacionCreate,
    CotizacionUpdate,
    CotizacionResponse
)
from datetime import datetime
from pathlib import Path
import logging
import os

from app.services.word_generator import word_generator
from app.services.pdf_generator import pdf_generator
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# ============================================
# FUNCIONES AUXILIARES
# ============================================

def generar_numero_cotizacion(db: Session) -> str:
    """
    Generar número único de cotización
    Formato: COT-YYYYMM-XXXX
    """
    fecha = datetime.now()
    prefijo = f"COT-{fecha.strftime('%Y%m')}"
    
    # Buscar última cotización del mes
    ultima = db.query(Cotizacion).filter(
        Cotizacion.numero.like(f"{prefijo}%")
    ).order_by(Cotizacion.numero.desc()).first()
    
    if ultima:
        try:
            ultimo_num = int(ultima.numero.split('-')[-1])
            nuevo_num = ultimo_num + 1
        except:
            nuevo_num = 1
    else:
        nuevo_num = 1
    
    return f"{prefijo}-{nuevo_num:04d}"

def _preparar_datos_documento(cotizacion: Cotizacion) -> Dict[str, Any]:
    """
    Helper para convertir un modelo de Cotizacion a un diccionario 
    para los generadores de Word/PDF.
    """
    items_list = []
    if cotizacion.items_rel:
        items_list = [
            {
                "descripcion": item.descripcion,
                "cantidad": float(item.cantidad),
                "precio_unitario": float(item.precio_unitario),
                "total": float(item.total)
            }
            for item in cotizacion.items_rel
        ]
    elif cotizacion.items:
        items_list = cotizacion.items

    datos = {
        "numero": cotizacion.numero,
        "cliente": cotizacion.cliente,
        "proyecto": cotizacion.proyecto,
        "fecha": cotizacion.fecha_creacion.strftime('%d/%m/%Y') if cotizacion.fecha_creacion else datetime.now().strftime('%d/%m/%Y'),
        "vigencia": cotizacion.vigencia or "30 días",
        "descripcion": cotizacion.descripcion or "",
        "observaciones": cotizacion.observaciones or "",
        "subtotal": float(cotizacion.subtotal) if cotizacion.subtotal else 0.00,
        "igv": float(cotizacion.igv) if cotizacion.igv else 0.00,
        "total": float(cotizacion.total) if cotizacion.total else 0.00,
        "items": items_list
    }
    return datos

# ============================================
# ENDPOINTS DE COTIZACIONES (CRUD)
# ============================================

@router.post("/", response_model=CotizacionResponse, status_code=status.HTTP_201_CREATED)
async def crear_cotizacion(
    cotizacion: CotizacionCreate,
    db: Session = Depends(get_db)
):
    """
    Crear una nueva cotización
    """
    
    try:
        # Generar número de cotización
        numero_cot = generar_numero_cotizacion(db)
        
        # ✅ CORRECCIÓN: Crear cotización con los campos correctos
        db_cotizacion = Cotizacion(
            numero=numero_cot,
            cliente=cotizacion.cliente,
            proyecto=cotizacion.proyecto,
            descripcion=cotizacion.descripcion,
            subtotal=cotizacion.subtotal,
            igv=cotizacion.igv,
            total=cotizacion.total,
            observaciones=cotizacion.observaciones,
            vigencia=cotizacion.vigencia,
            estado=cotizacion.estado or "borrador",
            items=cotizacion.items,  # Guardar items en JSON
            proyecto_id=cotizacion.proyecto_id,
            metadata_adicional=cotizacion.metadata_adicional
        )
        
        db.add(db_cotizacion)
        db.commit()
        db.refresh(db_cotizacion)
        
        # ✅ CORRECCIÓN: Crear items relacionados si existen
        if cotizacion.items:
            for item_data in cotizacion.items:
                # item_data es un dict, no tiene .dict()
                db_item = Item(
                    descripcion=item_data.get("descripcion"),
                    cantidad=item_data.get("cantidad"),
                    precio_unitario=item_data.get("precio_unitario"),
                    total=item_data.get("total", item_data.get("cantidad") * item_data.get("precio_unitario")),
                    cotizacion_id=db_cotizacion.id
                )
                db.add(db_item)
            
            db.commit()
            db.refresh(db_cotizacion)
        
        logger.info(f"✅ Cotización creada: {numero_cot}")
        return db_cotizacion
        
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error al crear cotización: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cotización: {str(e)}"
        )

@router.get("/", response_model=List[CotizacionResponse])
async def listar_cotizaciones(
    skip: int = 0,
    limit: int = 100,
    proyecto_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Listar todas las cotizaciones
    """
    query = db.query(Cotizacion)
    
    if proyecto_id:
        query = query.filter(Cotizacion.proyecto_id == proyecto_id)
        
    cotizaciones = query.order_by(Cotizacion.fecha_creacion.desc()).offset(skip).limit(limit).all()
    
    return cotizaciones

@router.get("/{cotizacion_id}", response_model=CotizacionResponse)
async def obtener_cotizacion(
    cotizacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener una cotización por ID
    """
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cotización no encontrada"
        )
    
    return cotizacion

@router.put("/{cotizacion_id}", response_model=CotizacionResponse)
async def actualizar_cotizacion(
    cotizacion_id: int,
    cotizacion_update: CotizacionUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar una cotización
    """
    
    db_cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not db_cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cotización no encontrada"
        )
    
    # Actualizar datos
    update_data = cotizacion_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key != "items":
            setattr(db_cotizacion, key, value)
    
    # Actualizar items si vienen
    if cotizacion_update.items is not None:
        # Eliminar items antiguos
        db.query(Item).filter(Item.cotizacion_id == cotizacion_id).delete()
        
        # Agregar items nuevos
        for item_data in cotizacion_update.items:
            db_item = Item(
                descripcion=item_data.get("descripcion"),
                cantidad=item_data.get("cantidad"),
                precio_unitario=item_data.get("precio_unitario"),
                total=item_data.get("total", item_data.get("cantidad") * item_data.get("precio_unitario")),
                cotizacion_id=cotizacion_id
            )
            db.add(db_item)
    
    db.commit()
    db.refresh(db_cotizacion)
    
    return db_cotizacion

@router.delete("/{cotizacion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_cotizacion(
    cotizacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar una cotización
    """
    db_cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not db_cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cotización no encontrada"
        )
    
    # Eliminar items asociados
    db.query(Item).filter(Item.cotizacion_id == cotizacion_id).delete()
    
    # Eliminar cotización
    db.delete(db_cotizacion)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# ============================================
# ENDPOINTS DE GENERACIÓN DE DOCUMENTOS
# ============================================

@router.post("/{cotizacion_id}/generar-pdf")
async def generar_pdf_cotizacion(
    cotizacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Genera un PDF profesional de la cotización
    """
    
    # Obtener cotización
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cotización no encontrada"
        )
    
    # Preparar datos
    datos = _preparar_datos_documento(cotizacion)
    
    # Definir ruta de salida
    nombre_archivo = f"{datos['numero']}_{datos['cliente']}.pdf"
    ruta_salida = os.path.join(settings.GENERATED_DIR, nombre_archivo)
    
    try:
        # Generar PDF
        pdf_generator.generar_cotizacion(
            datos=datos,
            ruta_salida=ruta_salida,
            opciones={'mostrar_logo': True}
        )
        
        if not os.path.exists(ruta_salida):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo generar el PDF"
            )
        
        logger.info(f"✅ PDF de cotización generado: {nombre_archivo}")
        
        return FileResponse(
            path=ruta_salida,
            filename=nombre_archivo,
            media_type="application/pdf"
        )
        
    except Exception as e:
        logger.error(f"Error al generar PDF: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar PDF: {str(e)}"
        )

@router.post("/{cotizacion_id}/generar-word")
async def generar_word_cotizacion(
    cotizacion_id: int,
    db: Session = Depends(get_db)
):
    """
    Genera un DOCX profesional de la cotización
    """
    
    # Obtener cotización
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    
    if not cotizacion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cotización no encontrada"
        )
    
    # Preparar datos
    datos = _preparar_datos_documento(cotizacion)
    
    # Definir ruta de salida
    nombre_archivo = f"{datos['numero']}_{datos['cliente']}.docx"
    ruta_salida = os.path.join(settings.GENERATED_DIR, nombre_archivo)
    
    try:
        # Generar Word
        word_generator.generar_cotizacion(
            datos=datos,
            ruta_salida=ruta_salida,
            opciones={'mostrar_logo': True}
        )
        
        if not os.path.exists(ruta_salida):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo generar el DOCX"
            )
        
        logger.info(f"✅ DOCX de cotización generado: {nombre_archivo}")
        
        return FileResponse(
            path=ruta_salida,
            filename=nombre_archivo,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except Exception as e:
        logger.error(f"Error al generar Word: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar Word: {str(e)}"
        )