from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import datetime
from pathlib import Path
import logging
import os

from app.core.database import get_db
from app.models import Proyecto, Cotizacion, Documento
from app.models.proyecto import EstadoProyecto
from app.schemas.proyecto import (
    ProyectoCreate,
    ProyectoUpdate,
    ProyectoResponse,
    ProyectoDraftCreate,
    ProyectoDraftUpdate
)

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=ProyectoResponse, status_code=status.HTTP_201_CREATED)
async def crear_proyecto(
    proyecto: ProyectoCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo proyecto
    """
    
    db_proyecto = Proyecto(
        nombre=proyecto.nombre,
        descripcion=proyecto.descripcion,
        cliente=proyecto.cliente,
        estado=EstadoProyecto.PLANIFICACION,
        # ✅ CAMPOS PMI
        servicio=proyecto.servicio,
        industria=proyecto.industria,
        presupuesto=proyecto.presupuesto,
        moneda=proyecto.moneda,
        duracion_total=proyecto.duracion_total,
        tipo_dias=proyecto.tipo_dias,
        area_m2=proyecto.area_m2,
        tiene_area=proyecto.tiene_area,
        alcance_proyecto=proyecto.alcance_proyecto,
        ubicacion=proyecto.ubicacion,
        normativa=proyecto.normativa,
        metadata_adicional=proyecto.metadata_adicional,
        fecha_inicio=datetime.utcnow()
    )
    
    db.add(db_proyecto)
    db.commit()
    db.refresh(db_proyecto)
    
    return db_proyecto

@router.post("/draft", response_model=ProyectoResponse, status_code=status.HTTP_201_CREATED)
async def crear_borrador_proyecto(
    proyecto: ProyectoDraftCreate,
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo proyecto en estado BORRADOR (todo opcional)
    """
    
    # Valores por defecto si no vienen
    nombre = proyecto.nombre or "Nuevo Proyecto (Borrador)"
    cliente = proyecto.cliente or "Sin Cliente Asignado"
    
    db_proyecto = Proyecto(
        nombre=nombre,
        cliente=cliente,
        estado=proyecto.estado, # Por defecto PLANIFICACION
        metadata_adicional=proyecto.metadata_adicional, # Aquí vive el estado de la UI
        fecha_inicio=datetime.utcnow()
    )
    
    db.add(db_proyecto)
    db.commit()
    db.refresh(db_proyecto)
    
    return db_proyecto

@router.patch("/{proyecto_id}/draft", response_model=ProyectoResponse)
async def actualizar_borrador_proyecto(
    proyecto_id: int,
    draft_update: ProyectoDraftUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un borrador (Ideal para Auto-Save del Frontend)
    """
    db_proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    
    if not db_proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
        
    # Actualizamos campos explícitos si vienen
    if draft_update.nombre:
        db_proyecto.nombre = draft_update.nombre
    if draft_update.cliente:
        db_proyecto.cliente = draft_update.cliente
    if draft_update.estado:
        db_proyecto.estado = draft_update.estado
    
    # Campos PMI
    if draft_update.servicio: db_proyecto.servicio = draft_update.servicio
    if draft_update.industria: db_proyecto.industria = draft_update.industria
    if draft_update.duracion_total: db_proyecto.duracion_total = draft_update.duracion_total
    
    # Metadata: MERGE o REPLACE?
    # Para simplificar y evitar conflictos de granularidad, REEMPLAZAMOS el dict de metadata
    # El Frontend debe enviar el estado completo de la UI en 'metadata_adicional'
    if draft_update.metadata_adicional is not None:
        db_proyecto.metadata_adicional = draft_update.metadata_adicional
        
    db_proyecto.fecha_modificacion = datetime.utcnow()
    
    db.commit()
    db.refresh(db_proyecto)
    
    return db_proyecto

@router.get("/", response_model=List[ProyectoResponse])
async def listar_proyectos(
    skip: int = 0,
    limit: int = 100,
    estado: Optional[EstadoProyecto] = None,
    cliente: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Lista todos los proyectos con filtros opcionales
    """
    
    query = db.query(Proyecto)
    
    # Aplicar filtros
    if estado:
        query = query.filter(Proyecto.estado == estado)
    
    if cliente:
        query = query.filter(Proyecto.cliente.ilike(f"%{cliente}%"))
    
    # Ordenar por fecha de creación
    query = query.order_by(Proyecto.fecha_creacion.desc())
    
    proyectos = query.offset(skip).limit(limit).all()
    
    return proyectos

@router.get("/{proyecto_id}", response_model=ProyectoResponse)
async def obtener_proyecto(
    proyecto_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un proyecto por ID con información completa
    """
    
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    return proyecto

@router.get("/{proyecto_id}/detalle")
async def obtener_proyecto_detallado(
    proyecto_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtiene un proyecto con todas sus relaciones (cotizaciones, documentos)
    """
    
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    # Obtener cotizaciones relacionadas
    cotizaciones = db.query(Cotizacion).filter(
        Cotizacion.proyecto_id == proyecto_id
    ).all()
    
    # Obtener documentos relacionados
    documentos = db.query(Documento).filter(
        Documento.proyecto_id == proyecto_id
    ).all()
    
    return {
        "proyecto": proyecto,
        "cotizaciones": cotizaciones,
        "documentos": documentos,
        "estadisticas": {
            "total_cotizaciones": len(cotizaciones),
            "total_documentos": len(documentos),
            "cotizaciones_aprobadas": sum(1 for c in cotizaciones if c.estado == "aprobada"),
            "valor_total": sum(c.total for c in cotizaciones if c.estado == "aprobada")
        }
    }

@router.put("/{proyecto_id}", response_model=ProyectoResponse)
async def actualizar_proyecto(
    proyecto_id: int,
    proyecto_update: ProyectoUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualiza un proyecto existente
    """
    
    db_proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    
    if not db_proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    # Actualizar campos
    update_data = proyecto_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_proyecto, field, value)
    
    db_proyecto.fecha_modificacion = datetime.utcnow()
    
    db.commit()
    db.refresh(db_proyecto)
    
    return db_proyecto

@router.delete("/{proyecto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_proyecto(
    proyecto_id: int,
    db: Session = Depends(get_db)
):
    """
    Elimina un proyecto
    NOTA: Esto también eliminará todas las cotizaciones y documentos relacionados
    """
    
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    db.delete(proyecto)
    db.commit()
    
    return None

@router.patch("/{proyecto_id}/estado")
async def cambiar_estado_proyecto(
    proyecto_id: int,
    nuevo_estado: EstadoProyecto,
    db: Session = Depends(get_db)
):
    """
    Cambia el estado de un proyecto
    """
    
    proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
    
    if not proyecto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    proyecto.estado = nuevo_estado
    proyecto.fecha_modificacion = datetime.utcnow()
    
    # Si se completa o cancela, establecer fecha de fin
    if nuevo_estado in [EstadoProyecto.COMPLETADO, EstadoProyecto.CANCELADO]:
        if not proyecto.fecha_fin:
            proyecto.fecha_fin = datetime.utcnow()
    
    db.commit()
    db.refresh(proyecto)
    
    return proyecto

@router.get("/stats/resumen")
async def obtener_estadisticas_proyectos(
    db: Session = Depends(get_db)
):
    """
    Obtiene estadísticas generales de proyectos
    """
    
    total = db.query(Proyecto).count()
    
    por_estado = {}
    for estado in EstadoProyecto:
        por_estado[estado.value] = db.query(Proyecto).filter(
            Proyecto.estado == estado
        ).count()
    
    return {
        "total_proyectos": total,
        "por_estado": por_estado
    }

# ════════════════════════════════════════════════════════════════
# ✅ ENDPOINTS MEJORADOS CON ANÁLISIS IA - INTEGRACIÓN report_generator
# ════════════════════════════════════════════════════════════════

@router.post("/{proyecto_id}/generar-informe-word")
async def generar_informe_proyecto_word(
    proyecto_id: int,
    incluir_cotizaciones: bool = Body(True),
    incluir_documentos: bool = Body(True),
    incluir_estadisticas: bool = Body(True),
    incluir_analisis_ia: bool = Body(True),  # ⭐ NUEVO
    opciones: Optional[Dict[str, bool]] = Body(None),
    logo_base64: Optional[str] = Body(None),
    usar_plantilla: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    """
    Genera un informe ejecutivo del proyecto en formato Word
    
    ⭐ MEJORADO CON IA - Ahora incluye análisis inteligente automático
    
    MODO COMPLEJO - Proyecto Complejo
    
    Incluye:
    - Información general del proyecto
    - Todas las cotizaciones asociadas
    - Documentos relacionados
    - ⭐ ANÁLISIS AUTOMÁTICO CON IA
    - ⭐ MÉTRICAS Y KPIs CALCULADOS
    - ⭐ CONCLUSIONES INTELIGENTES
    - ⭐ RECOMENDACIONES PERSONALIZADAS
    - ⭐ ANÁLISIS DE RIESGOS
    - Timeline del proyecto
    - Logo personalizado
    - Formato profesional
    
    Args:
        proyecto_id: ID del proyecto
        incluir_cotizaciones: Si incluir tabla de cotizaciones
        incluir_documentos: Si listar documentos del proyecto
        incluir_estadisticas: Si incluir gráficos y estadísticas
        incluir_analisis_ia: Si incluir análisis inteligente con IA ⭐ NUEVO
        opciones: Opciones de visualización
        logo_base64: Logo en base64
        usar_plantilla: Nombre de plantilla personalizada (opcional)
    
    Returns:
        Archivo Word para descarga
    """
    
    try:
        # Obtener proyecto
        proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
        
        if not proyecto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proyecto no encontrado"
            )
        
        logger.info(f"Generando informe Word INTELIGENTE para proyecto: {proyecto.nombre}")
        
        # Obtener cotizaciones relacionadas
        cotizaciones_db = db.query(Cotizacion).filter(
            Cotizacion.proyecto_id == proyecto_id
        ).all() if incluir_cotizaciones else []
        
        cotizaciones = []
        for cot in cotizaciones_db:
            cotizaciones.append({
                "numero": cot.numero,
                "cliente": cot.cliente,
                "proyecto": cot.proyecto,
                "estado": cot.estado,
                "subtotal": float(cot.subtotal) if cot.subtotal else 0,
                "igv": float(cot.igv) if cot.igv else 0,
                "total": float(cot.total) if cot.total else 0,
                "fecha_creacion": cot.fecha_creacion.strftime("%d/%m/%Y") if cot.fecha_creacion else "N/A"
            })
        
        # Obtener documentos relacionados
        documentos_db = db.query(Documento).filter(
            Documento.proyecto_id == proyecto_id
        ).all() if incluir_documentos else []
        
        documentos_info = []
        for doc in documentos_db:
            documentos_info.append({
                "nombre": doc.nombre_original,
                "tipo": doc.tipo_mime,
                "tamano_mb": round(doc.tamano / (1024 * 1024), 2),
                "fecha_subida": doc.fecha_subida.strftime("%d/%m/%Y") if doc.fecha_subida else "N/A",
                "procesado": "Sí" if doc.procesado == 1 else "No"
            })
        
        # ═══════════════════════════════════════════════════════
        # ⭐ ANÁLISIS INTELIGENTE CON report_generator
        # ═══════════════════════════════════════════════════════
        
        if incluir_analisis_ia:
            from app.services.report_generator import report_generator
            
            logger.info("🤖 Generando análisis inteligente con IA...")
            
            # Preparar datos del proyecto para análisis
            proyecto_dict = {
                "id": proyecto.id,
                "nombre": proyecto.nombre,
                "cliente": proyecto.cliente,
                "descripcion": proyecto.descripcion,
                "estado": proyecto.estado.value if hasattr(proyecto.estado, 'value') else str(proyecto.estado),
                "fecha_inicio": proyecto.fecha_inicio,
                "fecha_fin": proyecto.fecha_fin
            }
            
            # ⭐ GENERAR INFORME EJECUTIVO CON IA
            informe_completo = report_generator.generar_informe_ejecutivo_proyecto(
                proyecto_data=proyecto_dict,
                cotizaciones=cotizaciones,
                documentos=documentos_info,
                opciones=opciones or {}
            )
            
            logger.info("✅ Análisis inteligente completado")
            
            # Usar datos del informe completo (con análisis IA)
            datos_informe = informe_completo
            
        else:
            # Modo básico (sin IA)
            logger.info("Generando informe básico sin análisis IA")
            
            # Calcular estadísticas básicas
            total_cot = len(cotizaciones)
            aprobadas = sum(1 for c in cotizaciones if c.get('estado') == 'aprobada')
            valor_total = sum(c.get('total', 0) for c in cotizaciones if c.get('estado') == 'aprobada')
            
            datos_informe = {
                # Información del proyecto
                "cliente": proyecto.cliente,
                "proyecto": proyecto.nombre,
                "numero": f"PROY-{proyecto.id:04d}",
                "descripcion": proyecto.descripcion or "Sin descripción",
                
                # Metadata del proyecto
                "estado": proyecto.estado.value if hasattr(proyecto.estado, 'value') else str(proyecto.estado),
                "fecha_inicio": proyecto.fecha_inicio.strftime("%d/%m/%Y") if proyecto.fecha_inicio else "N/A",
                "fecha_fin": proyecto.fecha_fin.strftime("%d/%m/%Y") if proyecto.fecha_fin else "En curso",
                
                # Cotizaciones
                "cotizaciones": cotizaciones,
                
                # Documentos
                "documentos": documentos_info,
                
                # Estadísticas básicas
                "total_cotizaciones": total_cot,
                "cotizaciones_aprobadas": aprobadas,
                "total_documentos": len(documentos_info),
                "subtotal": valor_total,
                "igv": valor_total * 0.18,
                "total": valor_total * 1.18
            }
        
        # ═══════════════════════════════════════════════════════
        # GENERAR DOCUMENTO WORD
        # ═══════════════════════════════════════════════════════
        
        from app.services.word_generator import word_generator
        from app.core.config import settings
        
        # Nombre del archivo
        nombre_archivo = f"informe_proyecto_{proyecto.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        ruta_salida = os.path.join(settings.GENERATED_DIR, nombre_archivo)
        
        # Si hay plantilla personalizada, usar template_processor
        if usar_plantilla:
            from app.services.template_processor import template_processor
            
            ruta_plantilla = os.path.join(
                settings.TEMPLATES_DIR,
                usar_plantilla
            )
            
            if not os.path.exists(ruta_plantilla):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Plantilla no encontrada: {usar_plantilla}"
                )
            
            ruta_salida = template_processor.procesar_plantilla(
                ruta_plantilla=ruta_plantilla,
                datos_cotizacion=datos_informe,
                ruta_salida=ruta_salida,
                logo_base64=logo_base64
            )
        else:
            # Usar generador estándar
            word_generator.generar_informe_proyecto(
                datos=datos_informe,
                ruta_salida=ruta_salida,
                opciones=opciones or {},
                logo_base64=logo_base64
            )
        
        # Verificar que se creó el archivo
        if not os.path.exists(ruta_salida):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo generar el informe"
            )
        
        if incluir_analisis_ia:
            logger.info(f"✅ Informe INTELIGENTE generado: {nombre_archivo}")
        else:
            logger.info(f"✅ Informe básico generado: {nombre_archivo}")
        
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

@router.post("/{proyecto_id}/generar-informe-pdf")
async def generar_informe_proyecto_pdf(
    proyecto_id: int,
    incluir_cotizaciones: bool = Body(True),
    incluir_documentos: bool = Body(True),
    incluir_estadisticas: bool = Body(True),
    incluir_analisis_ia: bool = Body(True),  # ⭐ NUEVO
    opciones: Optional[Dict[str, bool]] = Body(None),
    logo_base64: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    """
    Genera un informe ejecutivo del proyecto en formato PDF
    
    ⭐ MEJORADO CON IA - Incluye análisis inteligente automático
    
    MODO COMPLEJO - Proyecto Complejo
    
    Similar al Word pero genera PDF (no editable)
    
    Args:
        proyecto_id: ID del proyecto
        incluir_cotizaciones: Si incluir tabla de cotizaciones
        incluir_documentos: Si listar documentos del proyecto
        incluir_estadisticas: Si incluir gráficos y estadísticas
        incluir_analisis_ia: Si incluir análisis inteligente ⭐ NUEVO
        opciones: Opciones de visualización
        logo_base64: Logo en base64
    
    Returns:
        Archivo PDF para descarga
    """
    
    try:
        # Obtener proyecto
        proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
        
        if not proyecto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proyecto no encontrado"
            )
        
        logger.info(f"Generando informe PDF INTELIGENTE para proyecto: {proyecto.nombre}")
        
        # Obtener cotizaciones relacionadas
        cotizaciones_db = db.query(Cotizacion).filter(
            Cotizacion.proyecto_id == proyecto_id
        ).all() if incluir_cotizaciones else []
        
        cotizaciones = []
        for cot in cotizaciones_db:
            cotizaciones.append({
                "numero": cot.numero,
                "estado": cot.estado,
                "total": float(cot.total) if cot.total else 0,
                "fecha_creacion": cot.fecha_creacion.strftime("%d/%m/%Y") if cot.fecha_creacion else "N/A"
            })
        
        # Obtener documentos relacionados
        documentos_db = db.query(Documento).filter(
            Documento.proyecto_id == proyecto_id
        ).all() if incluir_documentos else []
        
        documentos_info = []
        for doc in documentos_db:
            documentos_info.append({
                "nombre": doc.nombre_original,
                "tipo": doc.tipo_mime,
                "fecha": doc.fecha_subida.strftime("%d/%m/%Y") if doc.fecha_subida else "N/A"
            })
        
        # ⭐ ANÁLISIS INTELIGENTE (si está habilitado)
        if incluir_analisis_ia:
            from app.services.report_generator import report_generator
            
            logger.info("🤖 Generando análisis inteligente con IA...")
            
            proyecto_dict = {
                "id": proyecto.id,
                "nombre": proyecto.nombre,
                "cliente": proyecto.cliente,
                "descripcion": proyecto.descripcion,
                "estado": proyecto.estado.value if hasattr(proyecto.estado, 'value') else str(proyecto.estado),
                "fecha_inicio": proyecto.fecha_inicio,
                "fecha_fin": proyecto.fecha_fin
            }
            
            # Generar análisis completo
            informe_completo = report_generator.generar_informe_ejecutivo_proyecto(
                proyecto_data=proyecto_dict,
                cotizaciones=cotizaciones,
                documentos=documentos_info,
                opciones=opciones or {}
            )
            
            datos = informe_completo
            
        else:
            # Modo básico
            valor_total = sum(c.get('total', 0) for c in cotizaciones if c.get('estado') == 'aprobada')
            
            datos = {
                "nombre": proyecto.nombre,
                "descripcion": proyecto.descripcion,
                "cliente": proyecto.cliente,
                "estado": proyecto.estado.value if hasattr(proyecto.estado, 'value') else str(proyecto.estado),
                "fecha_inicio": proyecto.fecha_inicio,
                "fecha_fin": proyecto.fecha_fin,
                "cotizaciones": cotizaciones,
                "documentos": documentos_info,
                "valor_total": valor_total
            }
        
        # Generar PDF
        from app.services.pdf_generator import pdf_generator
        from app.core.config import settings
        
        nombre_archivo = f"informe_proyecto_{proyecto.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        ruta_salida = os.path.join(settings.GENERATED_DIR, nombre_archivo)
        
        pdf_generator.generar_informe_proyecto(
            datos=datos,
            ruta_salida=ruta_salida,
            opciones=opciones or {},
            logo_base64=logo_base64
        )
        
        if not os.path.exists(ruta_salida):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo generar el PDF"
            )
        
        logger.info(f"✅ PDF {'INTELIGENTE' if incluir_analisis_ia else 'básico'} generado: {nombre_archivo}")
        
        return FileResponse(
            path=ruta_salida,
            filename=nombre_archivo,
            media_type="application/pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al generar informe PDF: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar PDF: {str(e)}"
        )

# ════════════════════════════════════════════════════════════════
# ⭐ NUEVO ENDPOINT - OBTENER ANÁLISIS SIN GENERAR DOCUMENTO
# ════════════════════════════════════════════════════════════════

@router.get("/{proyecto_id}/analisis-ia")
async def obtener_analisis_ia_proyecto(
    proyecto_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener análisis inteligente del proyecto SIN generar documento
    
    ⭐ NUEVO - Solo retorna el análisis en JSON
    
    Útil para:
    - Preview del análisis antes de generar
    - Dashboard del proyecto
    - APIs que consumen el análisis
    
    Returns:
        JSON con análisis completo
    """
    
    try:
        # Obtener proyecto
        proyecto = db.query(Proyecto).filter(Proyecto.id == proyecto_id).first()
        
        if not proyecto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Proyecto no encontrado"
            )
        
        logger.info(f"Generando análisis IA para: {proyecto.nombre}")
        
        # Obtener cotizaciones
        cotizaciones_db = db.query(Cotizacion).filter(
            Cotizacion.proyecto_id == proyecto_id
        ).all()
        
        cotizaciones = []
        for cot in cotizaciones_db:
            cotizaciones.append({
                "numero": cot.numero,
                "estado": cot.estado,
                "total": float(cot.total) if cot.total else 0,
                "fecha_creacion": cot.fecha_creacion.strftime("%d/%m/%Y") if cot.fecha_creacion else "N/A"
            })
        
        # Obtener documentos
        documentos_db = db.query(Documento).filter(
            Documento.proyecto_id == proyecto_id
        ).all()
        
        documentos = []
        for doc in documentos_db:
            documentos.append({
                "nombre": doc.nombre_original,
                "tipo": doc.tipo_mime,
                "procesado": "Sí" if doc.procesado == 1 else "No"
            })
        
        # Generar análisis con IA
        from app.services.report_generator import report_generator
        
        proyecto_dict = {
            "id": proyecto.id,
            "nombre": proyecto.nombre,
            "cliente": proyecto.cliente,
            "descripcion": proyecto.descripcion,
            "estado": proyecto.estado.value if hasattr(proyecto.estado, 'value') else str(proyecto.estado),
            "fecha_inicio": proyecto.fecha_inicio,
            "fecha_fin": proyecto.fecha_fin
        }
        
        analisis = report_generator.generar_informe_ejecutivo_proyecto(
            proyecto_data=proyecto_dict,
            cotizaciones=cotizaciones,
            documentos=documentos,
            opciones={}
        )
        
        logger.info("✅ Análisis IA completado")
        
        return {
            "success": True,
            "proyecto_id": proyecto_id,
            "proyecto_nombre": proyecto.nombre,
            "analisis": analisis
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al generar análisis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al generar análisis: {str(e)}"
        )