"""
Token Manager - Gestor de límites de tokens para usuarios
Sistema de control de consumo con planes Free/Pro/Enterprise
"""
import logging
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.core.features import FeatureFlags

logger = logging.getLogger(__name__)


class TokenManager:
    """
    Gestor de tokens para usuarios

    Controla el consumo de tokens según el plan del usuario:
    - Free: 1,000 tokens/mes
    - Pro: 10,000 tokens/mes
    - Enterprise: 100,000 tokens/mes
    """

    # Estimaciones de tokens por tipo de operación
    TOKENS_CHAT = 150  # Chat conversacional
    TOKENS_COTIZACION_SIMPLE = 300  # Cotización simple
    TOKENS_COTIZACION_COMPLEJA = 800  # Cotización compleja
    TOKENS_PROYECTO = 1200  # Proyecto completo
    TOKENS_INFORME = 600  # Informe ejecutivo
    TOKENS_ANALISIS_DOCUMENTO = 400  # Análisis de documento

    def __init__(self, db: Session):
        self.db = db

    def verificar_tokens(self, usuario_id: int, tokens_requeridos: int) -> tuple[bool, str]:
        """
        Verifica si el usuario tiene tokens disponibles

        Args:
            usuario_id: ID del usuario
            tokens_requeridos: Cantidad de tokens que se necesitan

        Returns:
            (bool, str): (tiene_tokens, mensaje)
        """
        # Si el feature flag está OFF, siempre permitir (modo desarrollo)
        if not FeatureFlags.TOKEN_MANAGER:
            logger.info(f"🔓 TokenManager OFF - Permitiendo operación sin verificar tokens")
            return True, "Modo desarrollo - tokens ilimitados"

        # Buscar usuario
        usuario = self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            return False, "Usuario no encontrado"

        # Verificar si necesita reset de tokens (nuevo mes)
        if usuario.necesita_reset_tokens():
            usuario.resetear_tokens()
            self.db.commit()
            logger.info(f"🔄 Tokens reseteados para usuario {usuario.id} ({usuario.email})")

        # Verificar disponibilidad
        disponibles = usuario.tokens_disponibles()

        if disponibles >= tokens_requeridos:
            return True, f"Tokens disponibles: {disponibles:,}"
        else:
            faltante = tokens_requeridos - disponibles
            return False, f"Tokens insuficientes. Necesitas {faltante:,} más. Considera upgradearte a plan {self._sugerir_plan(usuario.plan)}"

    def consumir_tokens(self, usuario_id: int, tokens: int, operacion: str = "") -> bool:
        """
        Consume tokens del usuario

        Args:
            usuario_id: ID del usuario
            tokens: Cantidad de tokens a consumir
            operacion: Descripción de la operación (para logs)

        Returns:
            bool: True si se consumieron exitosamente
        """
        # Si el feature flag está OFF, no consumir (modo desarrollo)
        if not FeatureFlags.TOKEN_MANAGER:
            logger.info(f"🔓 TokenManager OFF - No consumiendo tokens")
            return True

        usuario = self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            logger.error(f"❌ Usuario {usuario_id} no encontrado")
            return False

        if usuario.consumir_tokens(tokens):
            self.db.commit()
            disponibles = usuario.tokens_disponibles()
            porcentaje_usado = (usuario.tokens_usados / usuario.tokens_mensuales) * 100

            logger.info(
                f"✅ Tokens consumidos: {tokens:,} | "
                f"Usuario: {usuario.email} | "
                f"Operación: {operacion} | "
                f"Disponibles: {disponibles:,} ({100-porcentaje_usado:.1f}% restante)"
            )

            # Alerta si está por acabarse los tokens
            if porcentaje_usado >= 90:
                logger.warning(
                    f"⚠️ Usuario {usuario.email} ha usado {porcentaje_usado:.1f}% de sus tokens"
                )

            return True
        else:
            logger.error(f"❌ No se pudieron consumir {tokens:,} tokens para usuario {usuario.email}")
            return False

    def get_estadisticas_usuario(self, usuario_id: int) -> dict:
        """Retorna estadísticas de tokens del usuario"""
        usuario = self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            return {}

        if usuario.necesita_reset_tokens():
            usuario.resetear_tokens()
            self.db.commit()

        disponibles = usuario.tokens_disponibles()
        porcentaje_usado = (usuario.tokens_usados / usuario.tokens_mensuales) * 100

        return {
            "plan": usuario.plan,
            "tokens_mensuales": usuario.tokens_mensuales,
            "tokens_usados": usuario.tokens_usados,
            "tokens_disponibles": disponibles,
            "tokens_extra": usuario.tokens_extra,
            "porcentaje_usado": round(porcentaje_usado, 2),
            "fecha_reset": usuario.fecha_reset_tokens.isoformat() if usuario.fecha_reset_tokens else None,
            "total_historico": usuario.total_tokens_historico,
        }

    def get_estadisticas_globales(self) -> dict:
        """Retorna estadísticas globales del sistema"""
        from sqlalchemy import func

        # Total usuarios
        total_usuarios = self.db.query(Usuario).count()

        # Usuarios por plan
        usuarios_free = self.db.query(Usuario).filter(Usuario.plan == "free").count()
        usuarios_pro = self.db.query(Usuario).filter(Usuario.plan == "pro").count()
        usuarios_enterprise = self.db.query(Usuario).filter(Usuario.plan == "enterprise").count()

        # Capacidad total
        capacidad_total = self.db.query(func.sum(Usuario.tokens_mensuales)).scalar() or 0
        tokens_usados = self.db.query(func.sum(Usuario.tokens_usados)).scalar() or 0
        tokens_disponibles = capacidad_total - tokens_usados

        # Tokens históricos
        tokens_historico = self.db.query(func.sum(Usuario.total_tokens_historico)).scalar() or 0

        return {
            "total_usuarios": total_usuarios,
            "usuarios_por_plan": {
                "free": usuarios_free,
                "pro": usuarios_pro,
                "enterprise": usuarios_enterprise
            },
            "capacidad_total": capacidad_total,
            "tokens_usados": tokens_usados,
            "tokens_disponibles": tokens_disponibles,
            "porcentaje_usado": round((tokens_usados / capacidad_total * 100), 2) if capacidad_total > 0 else 0,
            "tokens_historico": tokens_historico
        }

    def resetear_tokens_usuarios(self) -> int:
        """
        Resetea los tokens de TODOS los usuarios que necesitan reset
        Se ejecuta como cron job mensual

        Returns:
            int: Cantidad de usuarios reseteados
        """
        usuarios = self.db.query(Usuario).all()
        reseteados = 0

        for usuario in usuarios:
            if usuario.necesita_reset_tokens():
                usuario.resetear_tokens()
                reseteados += 1

        self.db.commit()
        logger.info(f"🔄 Reset mensual completado: {reseteados} usuarios reseteados")
        return reseteados

    def _sugerir_plan(self, plan_actual: str) -> str:
        """Sugiere un plan superior"""
        if plan_actual == "free":
            return "Pro ($29.99/mes)"
        elif plan_actual == "pro":
            return "Enterprise ($299/mes)"
        else:
            return "Enterprise (ya estás en el plan máximo)"

    def agregar_tokens_extra(self, usuario_id: int, tokens: int) -> bool:
        """
        Agrega tokens extra a un usuario (compra adicional)

        Args:
            usuario_id: ID del usuario
            tokens: Cantidad de tokens extra a agregar

        Returns:
            bool: True si se agregaron exitosamente
        """
        usuario = self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            return False

        usuario.tokens_extra += tokens
        self.db.commit()

        logger.info(f"💰 Tokens extra agregados: {tokens:,} para usuario {usuario.email}")
        return True
