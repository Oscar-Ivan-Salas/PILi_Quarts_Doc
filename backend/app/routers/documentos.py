"""
Router: Documentos
Endpoints para upload, procesamiento y búsqueda de documentos

🔧 VERSIÓN CORREGIDA - Restaurado código faltante en subir_documento
"""
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query, Body
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from app.core.database import get_db
from app.models.documento import Documento
from app.schemas.documento import (
    DocumentoResponse,
    DocumentoUploadResponse,
    BusquedaSemanticaRequest,
    ResultadoBusqueda
)
from app.services.file_processor import file_processor
from app.services.rag_service import rag_service
from app.services.gemini_service import gemini_service
from app.core.config import settings
from pathlib import Path
from datetime import datetime
import shutil
import uuid
import logging
import os
import filetype  # 🔧 IMPORT AGREGADO - Requerido para detección MIME

logger = logging.getLogger(__name__)

router = APIRouter()

# ============================================
# ENDPOINTS DE DOCUMENTOS
# ============================================

@router.post("/upload", response_model=DocumentoUploadResponse)
async def subir_documento(
    archivo: UploadFile = File(...),
    proyecto_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Subir y procesar un documento
    
    Soporta: PDF, Word, Excel, imágenes, texto
    
    🔧 CÓDIGO CORREGIDO - Restauradas líneas 65-102 que faltaban
    """
    try:
        logger.info(f"Subiendo archivo: {archivo.filename}")
        
        # Validar archivo
        es_valido, mensaje_error = file_processor.validar_archivo(
            nombre_archivo=archivo.filename,
            tamano=0  # Se validará después de leer
        )
        
        if not es_valido:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=mensaje_error
            )
        
        # Leer contenido del archivo
        contenido = await archivo.read()
        tamano = len(contenido)
        
        # 🔧 CÓDIGO RESTAURADO - Validar tamaño después de leer
        if tamano > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Archivo demasiado grande. Máximo: {settings.MAX_FILE_SIZE / (1024*1024):.1f} MB"
            )
        
        # 🔧 CÓDIGO RESTAURADO - Generar nombre único
        extension = Path(archivo.filename).suffix
        nombre_unico = f"{uuid.uuid4()}{extension}"
        ruta_archivo = Path(settings.UPLOAD_DIR) / nombre_unico
        
        # 🔧 CÓDIGO RESTAURADO - Asegurar que el directorio existe
        Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        
        # 🔧 CÓDIGO RESTAURADO - Guardar archivo físicamente
        with open(ruta_archivo, "wb") as f:
            f.write(contenido)
        
        # 🔧 CÓDIGO RESTAURADO - Detectar tipo MIME usando filetype
        tipo_mime = archivo.content_type or "application/octet-stream"
        try:
            kind = filetype.guess(str(ruta_archivo))
            if kind is not None:
                tipo_mime = kind.mime
        except Exception:
            pass  # Usar el tipo MIME del archivo original
        
        # 🔧 CÓDIGO RESTAURADO - Crear registro en base de datos
        documento = Documento(
            nombre_original=archivo.filename,
            ruta_archivo=str(ruta_archivo),
            tipo_mime=tipo_mime,
            tamano=tamano,
            procesado=0,  # Pendiente
            proyecto_id=proyecto_id
        )
        db.add(documento)
        db.commit()
        db.refresh(documento)
        
        # 🔧 CÓDIGO RESTAURADO - Procesar archivo en segundo plano
        try:
            resultado = file_processor.procesar_archivo(str(ruta_archivo))
            
            # ✅ CÓDIGO EXISTENTE CONSERVADO - Actualizar con resultados
            documento.contenido_texto = resultado.get('contenido', '')
            documento.metadata_extraida = resultado.get('metadata', {})
            documento.procesado = 1  # Procesado exitosamente
            
            # Agregar a RAG (búsqueda semántica)
            if documento.contenido_texto and len(documento.contenido_texto.strip()) > 10:
                rag_service.agregar_documento(
                    documento_id=documento.id,
                    contenido=documento.contenido_texto,
                    metadata={
                        "nombre": archivo.filename,
                        "tipo": tipo_mime,
                        "proyecto_id": proyecto_id
                    }
                )
            
            db.commit()
            db.refresh(documento)
            
            logger.info(f"Documento procesado exitosamente: {archivo.filename}")
            
            return DocumentoUploadResponse(
                success=True,
                message="Documento subido y procesado exitosamente",
                documento=documento,
                contenido_extraido=documento.contenido_texto[:500] if documento.contenido_texto else None
            )
            
        except Exception as e:
            # Marcar como error pero mantener el archivo
            documento.procesado = 2  # Error
            documento.mensaje_error = str(e)
            db.commit()
            
            logger.warning(f"Error al procesar documento {archivo.filename}: {str(e)}")
            
            return DocumentoUploadResponse(
                success=True,
                message=f"Documento subido pero hubo un error al procesarlo: {str(e)}",
                documento=documento,
                contenido_extraido=None
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al subir documento: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al subir documento: {str(e)}"
        )

@router.get("/", response_model=List[DocumentoResponse])
def listar_documentos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    proyecto_id: Optional[int] = Query(None),
    procesado: Optional[int] = Query(None, ge=0, le=2),
    db: Session = Depends(get_db)
):
    """
    Listar documentos con filtros
    """
    try:
        query = db.query(Documento)
        
        if proyecto_id:
            query = query.filter(Documento.proyecto_id == proyecto_id)
        
        if procesado is not None:
            query = query.filter(Documento.procesado == procesado)
        
        documentos = query.order_by(Documento.fecha_subida.desc()).offset(skip).limit(limit).all()
        
        return documentos
        
    except Exception as e:
        logger.error(f"Error al listar documentos: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar documentos: {str(e)}"
        )

@router.get("/{documento_id}", response_model=DocumentoResponse)
def obtener_documento(
    documento_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener documento por ID
    """
    documento = db.query(Documento).filter(Documento.id == documento_id).first()
    
    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documento con ID {documento_id} no encontrado"
        )
    
    return documento

@router.delete("/{documento_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_documento(
    documento_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar documento
    """
    documento = db.query(Documento).filter(Documento.id == documento_id).first()
    
    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Documento con ID {documento_id} no encontrado"
        )
    
    try:
        # Eliminar archivo físico
        ruta_archivo = Path(documento.ruta_archivo)
        if ruta_archivo.exists():
            ruta_archivo.unlink()
        
        # Eliminar de RAG
        rag_service.eliminar_documento(documento_id)
        
        # Eliminar de base de datos
        db.delete(documento)
        db.commit()
        
        logger.info(f"Documento eliminado: {documento.nombre_original}")
        
        return None
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error al eliminar documento: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar documento: {str(e)}"
        )

@router.post("/buscar-semantica")
def buscar_semantica(
    request: BusquedaSemanticaRequest,
    db: Session = Depends(get_db)
):
    """
    Búsqueda semántica en documentos usando RAG
    
    Encuentra documentos relevantes basándose en el significado,
    no solo palabras clave
    """
    try:
        logger.info(f"Búsqueda semántica: {request.query}")
        
        # Buscar en RAG
        filtro = None
        if request.proyecto_id:
            filtro = {"proyecto_id": request.proyecto_id}
        
        resultados = rag_service.buscar_similar(
            query=request.query,
            limite=request.limite,
            filtro_metadata=filtro
        )
        
        # Obtener información completa de documentos
        documentos_encontrados = []
        for resultado in resultados:
            documento_id = resultado.get("metadata", {}).get("documento_id")
            if documento_id:
                documento = db.query(Documento).filter(Documento.id == documento_id).first()
                if documento:
                    documentos_encontrados.append({
                        "documento": documento,
                        "score": resultado.get("score", 0),
                        "fragmento": resultado.get("contenido", "")[:200]
                    })
        
        return {
            "success": True,
            "query": request.query,
            "total_encontrados": len(documentos_encontrados),
            "documentos": documentos_encontrados
        }
        
    except Exception as e:
        logger.error(f"Error en búsqueda semántica: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en búsqueda: {str(e)}"
        )

@router.post("/{documento_id}/reprocesar")
def reprocesar_documento(
    documento_id: int,
    db: Session = Depends(get_db)
):
    """
    Reprocesar un documento que tuvo errores
    """
    documento = db.query(Documento).filter(Documento.id == documento_id).first()
    
    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado"
        )
    
    try:
        logger.info(f"Reprocesando documento: {documento.nombre_original}")
        
        # Procesar de nuevo
        resultado = file_processor.procesar_archivo(documento.ruta_archivo)
        
        # Actualizar contenido
        documento.contenido_texto = resultado.get('contenido', '')
        documento.metadata_extraida = resultado.get('metadata', {})
        documento.procesado = 1
        documento.mensaje_error = None
        
        # Agregar/actualizar en RAG
        if documento.contenido_texto and len(documento.contenido_texto.strip()) > 10:
            # Primero eliminar si ya existía
            rag_service.eliminar_documento(documento.id)
            
            # Agregar de nuevo con contenido actualizado
            rag_service.agregar_documento(
                documento_id=documento.id,
                contenido=documento.contenido_texto,
                metadata={
                    "nombre": documento.nombre_original,
                    "tipo": documento.tipo_mime,
                    "proyecto_id": documento.proyecto_id
                }
            )
        
        db.commit()
        
        logger.info(f"Documento reprocesado exitosamente: {documento.nombre_original}")
        
        return {
            "success": True,
            "message": "Documento reprocesado exitosamente",
            "contenido_extraido": documento.contenido_texto[:500] if documento.contenido_texto else None
        }
        
    except Exception as e:
        # Marcar como error
        documento.procesado = 2
        documento.mensaje_error = str(e)
        db.commit()
        
        logger.error(f"Error al reprocesar documento: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al reprocesar: {str(e)}"
        )

@router.post("/{documento_id}/analizar-con-ia")
def analizar_documento_con_ia(
    documento_id: int,
    tipo_analisis: str = Body("completo"),
    db: Session = Depends(get_db)
):
    """
    Analizar documento usando IA (Gemini)
    
    Tipos de análisis:
    - completo: Análisis detallado
    - resumen: Solo resumen ejecutivo
    - tecnico: Análisis técnico especializado
    """
    documento = db.query(Documento).filter(Documento.id == documento_id).first()
    
    if not documento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documento no encontrado"
        )
    
    if not documento.contenido_texto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El documento no tiene contenido procesado. Ejecuta /reprocesar primero."
        )
    
    try:
        logger.info(f"Analizando documento con IA: {documento.nombre_original}")
        
        # Analizar con Gemini
        resultado_analisis = gemini_service.analizar_documento(
            texto_documento=documento.contenido_texto,
            tipo_analisis=tipo_analisis
        )
        
        # Actualizar metadata con análisis
        if documento.metadata_extraida:
            documento.metadata_extraida["analisis_ia"] = resultado_analisis
        else:
            documento.metadata_extraida = {"analisis_ia": resultado_analisis}
        
        db.commit()
        
        logger.info(f"Análisis IA completado para: {documento.nombre_original}")
        
        return {
            "success": True,
            "tipo_analisis": tipo_analisis,
            "documento": {
                "id": documento.id,
                "nombre": documento.nombre_original
            },
            "analisis": resultado_analisis
        }
        
    except Exception as e:
        logger.error(f"Error en análisis IA: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en análisis: {str(e)}"
        )

@router.get("/estadisticas/rag")
def obtener_estadisticas_rag():
    """
    Obtener estadísticas del sistema RAG
    """
    try:
        estadisticas = rag_service.obtener_estadisticas()
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "estadisticas": estadisticas
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas RAG: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo estadísticas: {str(e)}"
        )

# ============================================
# 🔧 ENDPOINTS DE GENERACIÓN DE INFORMES
# ============================================

@router.post("/{documento_id}/generar-informe-analisis-word")
async def generar_informe_analisis_word(
    documento_id: int,
    incluir_contenido_completo: bool = Body(False),
    incluir_metadata: bool = Body(True),
    opciones: Optional[Dict[str, bool]] = Body(None),
    logo_base64: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    """
    Generar informe de análisis del documento en formato Word
    
    MODO COMPLEJO - Para análisis detallado de documentos
    
    Incluye:
    - Información del documento
    - Análisis realizado por IA (Gemini)
    - Extracción de datos clave
    - Conclusiones y recomendaciones
    - Metadata del archivo
    - Logo personalizado
    
    Args:
        documento_id: ID del documento
        incluir_contenido_completo: Si incluir todo el texto extraído
        incluir_metadata: Si incluir metadata del archivo
        opciones: Opciones de visualización
        logo_base64: Logo en base64
    
    Returns:
        Archivo Word para descarga
    """
    
    try:
        # Obtener documento
        documento = db.query(Documento).filter(Documento.id == documento_id).first()
        
        if not documento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Documento no encontrado"
            )
        
        if not documento.contenido_texto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El documento no tiene contenido procesado. Ejecuta /reprocesar primero."
            )
        
        logger.info(f"Generando informe de análisis Word para: {documento.nombre_original}")
        
        # Analizar con IA
        analisis_ia = gemini_service.analizar_documento(
            texto_documento=documento.contenido_texto,
            tipo_analisis="completo"
        )
        
        # Preparar datos del informe
        datos_informe = {
            # Información del documento
            "numero": f"DOC-{documento.id:04d}",
            "cliente": "Sistema Tesla",  # Placeholder
            "proyecto": f"Análisis de {documento.nombre_original}",
            
            # Metadata del documento
            "nombre_archivo": documento.nombre_original,
            "tipo_archivo": documento.tipo_mime,
            "tamano_mb": round(documento.tamano / (1024 * 1024), 2),
            "fecha_subida": documento.fecha_subida.strftime("%d/%m/%Y %H:%M") if documento.fecha_subida else "N/A",
            "estado_procesamiento": "Procesado" if documento.procesado == 1 else "Error",
            
            # Análisis de IA
            "descripcion": analisis_ia.get('resumen', 'Análisis completado con IA Gemini'),
            "analisis_completo": analisis_ia,
            
            # Contenido
            "contenido_extracto": documento.contenido_texto[:2000] if documento.contenido_texto else "",
            "contenido_completo": documento.contenido_texto if incluir_contenido_completo else None,
            
            # Metadata extraída
            "metadata_extraida": documento.metadata_extraida if incluir_metadata else {},
            
            # Items para tabla (si hay)
            "items": []
        }
        
        # Si el análisis incluye items/puntos clave, agregarlos
        if analisis_ia.get('puntos_clave'):
            for i, punto in enumerate(analisis_ia.get('puntos_clave', []), 1):
                datos_informe["items"].append({
                    "descripcion": punto,
                    "cantidad": 1,
                    "precio_unitario": 0,
                })
        
        # Generar documento Word
        from app.services.word_generator import word_generator
        
        nombre_archivo = f"analisis_{documento.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        ruta_salida = os.path.join(settings.GENERATED_DIR, nombre_archivo)
        
        # Usar el generador estándar adaptado
        word_generator.generar_cotizacion(
            datos=datos_informe,
            ruta_salida=ruta_salida,
            opciones=opciones or {
                'mostrar_precios': False,
                'mostrar_igv': False,
                'mostrar_observaciones': True,
                'mostrar_logo': True
            },
            logo_base64=logo_base64
        )
        
        if not os.path.exists(ruta_salida):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo generar el informe"
            )
        
        logger.info(f"✅ Informe de análisis generado: {nombre_archivo}")
        
        return FileResponse(
            path=ruta_salida,
            filename=nombre_archivo,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al generar informe Word: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar informe: {str(e)}"
        )

@router.post("/{documento_id}/generar-informe-analisis-pdf")
async def generar_informe_analisis_pdf(
    documento_id: int,
    incluir_contenido_completo: bool = Body(False),
    incluir_metadata: bool = Body(True),
    opciones: Optional[Dict[str, bool]] = Body(None),
    logo_base64: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    """
    Generar informe de análisis del documento en formato PDF
    
    MODO COMPLEJO - Para análisis detallado de documentos
    
    Similar al Word pero genera PDF (no editable)
    
    Args:
        documento_id: ID del documento
        incluir_contenido_completo: Si incluir todo el texto extraído
        incluir_metadata: Si incluir metadata del archivo
        opciones: Opciones de visualización
        logo_base64: Logo en base64
    
    Returns:
        Archivo PDF para descarga
    """
    
    try:
        # Obtener documento
        documento = db.query(Documento).filter(Documento.id == documento_id).first()
        
        if not documento:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Documento no encontrado"
            )
        
        if not documento.contenido_texto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El documento no tiene contenido procesado"
            )
        
        logger.info(f"Generando informe de análisis PDF para: {documento.nombre_original}")
        
        # Analizar con IA
        analisis_ia = gemini_service.analizar_documento(
            texto_documento=documento.contenido_texto,
            tipo_analisis="completo"
        )
        
        # Preparar datos
        datos_informe = {
            "numero": f"DOC-{documento.id:04d}",
            "cliente": "Sistema Tesla",
            "proyecto": f"Análisis de {documento.nombre_original}",
            "descripcion": analisis_ia.get('resumen', 'Análisis con IA'),
            "items": []
        }
        
        # Generar PDF
        from app.services.pdf_generator import pdf_generator
        
        nombre_archivo = f"analisis_{documento.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        ruta_salida = os.path.join(settings.GENERATED_DIR, nombre_archivo)
        
        pdf_generator.generar_cotizacion(
            datos=datos_informe,
            ruta_salida=ruta_salida,
            opciones=opciones or {
                'mostrar_precios': False,
                'mostrar_igv': False,
                'mostrar_observaciones': True,
                'mostrar_logo': True
            },
            logo_base64=logo_base64
        )
        
        if not os.path.exists(ruta_salida):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo generar el PDF"
            )
        
        logger.info(f"✅ PDF de análisis generado: {nombre_archivo}")
        
        return FileResponse(
            path=ruta_salida,
            filename=nombre_archivo,
            media_type="application/pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al generar PDF: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar PDF: {str(e)}"
        )

# ============================================
# 🆕 ENDPOINT DE GENERACIÓN DE PROYECTOS
# ============================================

@router.post("/generar-proyecto")
async def generar_proyecto(
    datos: Dict = Body(...),
    personalizacion: Optional[Dict] = Body(None),
    tipo: str = Body("simple")  # "simple" o "complejo"
):
    """
    Generar documento de proyecto (Simple o Complejo)
    
    Args:
        datos: Datos del proyecto generados por el chatbot
        personalizacion: Configuración de personalización (logo, colores, fuente)
        tipo: Tipo de proyecto ("simple" o "complejo")
    
    Returns:
        Archivo Word para descarga
    """
    try:
        logger.info(f"Generando proyecto {tipo}: {datos.get('numero', 'SIN-CODIGO')}")
        
        # Generar documento Word usando el generador existente
        from app.services.word_generator import word_generator
        
        nombre_archivo = f"proyecto_{datos.get('numero', 'PROY')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        ruta_salida = os.path.join(settings.GENERATED_DIR, nombre_archivo)
        
        # Asegurar que el directorio existe
        os.makedirs(settings.GENERATED_DIR, exist_ok=True)
        
        # Preparar opciones de personalización
        opciones = {
            'mostrar_logo': personalizacion.get('mostrar_logo', True) if personalizacion else True,
            'esquema_colores': personalizacion.get('esquema_colores', 'azul-tesla') if personalizacion else 'azul-tesla',
            'fuente': personalizacion.get('fuente', 'Calibri') if personalizacion else 'Calibri'
        }
        
        # Logo en base64
        logo_base64 = personalizacion.get('logo_base64') if personalizacion else None
        
        # Generar documento
        word_generator.generar_proyecto(
            datos=datos,
            ruta_salida=ruta_salida,
            tipo=tipo,
            opciones=opciones,
            logo_base64=logo_base64
        )
        
        if not os.path.exists(ruta_salida):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo generar el documento"
            )
        
        logger.info(f"✅ Proyecto generado: {nombre_archivo}")
        
        return FileResponse(
            path=ruta_salida,
            filename=nombre_archivo,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al generar proyecto: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar proyecto: {str(e)}"
        )
