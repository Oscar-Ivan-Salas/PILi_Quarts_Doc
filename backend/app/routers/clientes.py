"""
Router: Clientes
Endpoints para CRUD completo de clientes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path as PathParam
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.core.database import get_db
from app.models.cliente import Cliente
from app.schemas.cliente import (
    ClienteCreate,
    ClienteUpdate,
    ClienteResponse,
    ClienteListResponse
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# ============================================
# ENDPOINTS DE CLIENTES (CRUD)
# ============================================

@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
async def crear_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo cliente

    Args:
        cliente: Datos del cliente a crear
        db: Sesión de base de datos

    Returns:
        Cliente creado

    Raises:
        HTTPException 400: Si el RUC ya existe
    """
    try:
        logger.info(f"Creando cliente: {cliente.nombre} - RUC: {cliente.ruc}")

        # Verificar que el RUC no exista
        existe = db.query(Cliente).filter(Cliente.ruc == cliente.ruc).first()
        if existe:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un cliente con el RUC {cliente.ruc}"
            )

        # Crear nuevo cliente (solo con campos proporcionados)
        db_cliente = Cliente(**cliente.model_dump(exclude_unset=True))
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)

        logger.info(f"✅ Cliente creado: ID={db_cliente.id}, {db_cliente.nombre}")
        return db_cliente

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error creando cliente: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cliente: {str(e)}"
        )

@router.get("/", response_model=List[ClienteListResponse])
async def listar_clientes(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de registros"),
    buscar: Optional[str] = Query(None, description="Buscar por nombre, RUC o email"),
    activo: Optional[str] = Query(None, description="Filtrar por estado (activo/inactivo)"),
    industria: Optional[str] = Query(None, description="Filtrar por industria"),
    db: Session = Depends(get_db)
):
    """
    Listar clientes con paginación y filtros

    Args:
        skip: Registros a omitir (para paginación)
        limit: Máximo de registros a retornar
        buscar: Texto para buscar en nombre, RUC o email
        activo: Filtrar por estado
        industria: Filtrar por industria
        db: Sesión de base de datos

    Returns:
        Lista de clientes
    """
    try:
        logger.info(f"Listando clientes: skip={skip}, limit={limit}, buscar={buscar}")

        # Construir query base
        query = db.query(Cliente)

        # Aplicar filtros
        if buscar:
            query = query.filter(
                or_(
                    Cliente.nombre.ilike(f"%{buscar}%"),
                    Cliente.ruc.ilike(f"%{buscar}%"),
                    Cliente.email.ilike(f"%{buscar}%")
                )
            )

        if activo:
            query = query.filter(Cliente.activo == activo)

        if industria:
            query = query.filter(Cliente.industria == industria)

        # Ordenar por fecha de creación (más recientes primero)
        query = query.order_by(Cliente.fecha_creacion.desc())

        # Aplicar paginación
        clientes = query.offset(skip).limit(limit).all()

        logger.info(f"✅ Se encontraron {len(clientes)} clientes")
        return clientes

    except Exception as e:
        logger.error(f"❌ Error listando clientes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al listar clientes: {str(e)}"
        )

@router.get("/{cliente_id}", response_model=ClienteResponse)
async def obtener_cliente(
    cliente_id: int = PathParam(..., description="ID del cliente"),
    db: Session = Depends(get_db)
):
    """
    Obtener un cliente por ID

    Args:
        cliente_id: ID del cliente
        db: Sesión de base de datos

    Returns:
        Cliente encontrado

    Raises:
        HTTPException 404: Si el cliente no existe
    """
    try:
        logger.info(f"Obteniendo cliente ID: {cliente_id}")

        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cliente_id} no encontrado"
            )

        logger.info(f"✅ Cliente encontrado: {cliente.nombre}")
        return cliente

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error obteniendo cliente: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente: {str(e)}"
        )

@router.get("/ruc/{ruc}", response_model=ClienteResponse)
async def obtener_cliente_por_ruc(
    ruc: str = PathParam(..., description="RUC del cliente"),
    db: Session = Depends(get_db)
):
    """
    Obtener un cliente por RUC

    Args:
        ruc: RUC del cliente
        db: Sesión de base de datos

    Returns:
        Cliente encontrado

    Raises:
        HTTPException 404: Si el cliente no existe
    """
    try:
        logger.info(f"Buscando cliente por RUC: {ruc}")

        cliente = db.query(Cliente).filter(Cliente.ruc == ruc).first()

        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con RUC {ruc} no encontrado"
            )

        logger.info(f"✅ Cliente encontrado: {cliente.nombre}")
        return cliente

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error obteniendo cliente por RUC: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cliente: {str(e)}"
        )

@router.put("/{cliente_id}", response_model=ClienteResponse)
async def actualizar_cliente(
    cliente_id: int = PathParam(..., description="ID del cliente"),
    cliente_update: ClienteUpdate = ...,
    db: Session = Depends(get_db)
):
    """
    Actualizar un cliente existente

    Args:
        cliente_id: ID del cliente a actualizar
        cliente_update: Datos a actualizar
        db: Sesión de base de datos

    Returns:
        Cliente actualizado

    Raises:
        HTTPException 404: Si el cliente no existe
        HTTPException 400: Si el RUC ya existe para otro cliente
    """
    try:
        logger.info(f"Actualizando cliente ID: {cliente_id}")

        # Buscar cliente
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cliente_id} no encontrado"
            )

        # Verificar RUC si se está actualizando
        if cliente_update.ruc and cliente_update.ruc != cliente.ruc:
            existe = db.query(Cliente).filter(
                Cliente.ruc == cliente_update.ruc,
                Cliente.id != cliente_id
            ).first()
            if existe:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Ya existe otro cliente con el RUC {cliente_update.ruc}"
                )

        # Actualizar campos (solo los que no son None)
        update_data = cliente_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(cliente, field, value)

        db.commit()
        db.refresh(cliente)

        logger.info(f"✅ Cliente actualizado: {cliente.nombre}")
        return cliente

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error actualizando cliente: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cliente: {str(e)}"
        )

@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_cliente(
    cliente_id: int = PathParam(..., description="ID del cliente"),
    db: Session = Depends(get_db)
):
    """
    Eliminar un cliente (soft delete, marca como inactivo)

    Args:
        cliente_id: ID del cliente a eliminar
        db: Sesión de base de datos

    Returns:
        204 No Content

    Raises:
        HTTPException 404: Si el cliente no existe
    """
    try:
        logger.info(f"Eliminando cliente ID: {cliente_id}")

        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cliente_id} no encontrado"
            )

        # Soft delete: marcar como inactivo
        cliente.activo = "inactivo"
        db.commit()

        logger.info(f"✅ Cliente marcado como inactivo: {cliente.nombre}")
        return None

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error eliminando cliente: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar cliente: {str(e)}"
        )

@router.post("/{cliente_id}/activar", response_model=ClienteResponse)
async def activar_cliente(
    cliente_id: int = PathParam(..., description="ID del cliente"),
    db: Session = Depends(get_db)
):
    """
    Reactivar un cliente inactivo

    Args:
        cliente_id: ID del cliente
        db: Sesión de base de datos

    Returns:
        Cliente reactivado

    Raises:
        HTTPException 404: Si el cliente no existe
    """
    try:
        logger.info(f"Reactivando cliente ID: {cliente_id}")

        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()

        if not cliente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cliente con ID {cliente_id} no encontrado"
            )

        cliente.activo = "activo"
        db.commit()
        db.refresh(cliente)

        logger.info(f"✅ Cliente reactivado: {cliente.nombre}")
        return cliente

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"❌ Error reactivando cliente: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al reactivar cliente: {str(e)}"
        )
