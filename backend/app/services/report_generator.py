"""
═══════════════════════════════════════════════════════════════
REPORT GENERATOR - Generador Avanzado de Informes Ejecutivos
═══════════════════════════════════════════════════════════════

PROPÓSITO:
Servicio especializado en generar informes ejecutivos complejos
que combinan datos del proyecto, análisis de IA, estadísticas
y visualizaciones profesionales.

CARACTERÍSTICAS:
- Análisis automático con IA
- Generación de conclusiones inteligentes
- Cálculo de métricas y KPIs
- Recomendaciones basadas en datos
- Formato ejecutivo profesional

DIFERENCIA CON word_generator y pdf_generator:
- word_generator: Genera documentos básicos
- pdf_generator: Genera PDFs básicos
- report_generator: Orquesta todo + análisis IA + métricas

═══════════════════════════════════════════════════════════════
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ReportGenerator:
    """
    Generador avanzado de informes ejecutivos
    
    Combina:
    - Datos del proyecto/cotización
    - Análisis de IA (Gemini)
    - Cálculo de métricas
    - Generación de recomendaciones
    """
    
    def __init__(self):
        """Inicializar generador"""
        logger.info("ReportGenerator inicializado")
    
    # ════════════════════════════════════════════════════════
    # FUNCIÓN PRINCIPAL - INFORME EJECUTIVO DE PROYECTO
    # ════════════════════════════════════════════════════════
    
    def generar_informe_ejecutivo_proyecto(
        self,
        proyecto_data: Dict[str, Any],
        cotizaciones: List[Dict[str, Any]],
        documentos: List[Dict[str, Any]],
        opciones: Optional[Dict[str, bool]] = None
    ) -> Dict[str, Any]:
        """
        Generar informe ejecutivo completo de proyecto
        
        Este método PREPARA los datos con análisis avanzado.
        Luego word_generator o pdf_generator usan estos datos.
        
        Args:
            proyecto_data: Datos del proyecto
            cotizaciones: Lista de cotizaciones asociadas
            documentos: Lista de documentos del proyecto
            opciones: Opciones de generación
        
        Returns:
            Dict con datos estructurados para el informe
        """
        
        try:
            logger.info(f"Generando informe ejecutivo para: {proyecto_data.get('nombre', 'N/A')}")
            
            # 1. Calcular métricas del proyecto
            metricas = self._calcular_metricas_proyecto(proyecto_data, cotizaciones, documentos)
            
            # 2. Analizar estado del proyecto
            analisis_estado = self._analizar_estado_proyecto(proyecto_data, metricas)
            
            # 3. Generar conclusiones con IA
            conclusiones = self._generar_conclusiones_ia(proyecto_data, metricas, analisis_estado)
            
            # 4. Generar recomendaciones
            recomendaciones = self._generar_recomendaciones(proyecto_data, metricas, analisis_estado)
            
            # 5. Preparar timeline del proyecto
            timeline = self._generar_timeline(proyecto_data, cotizaciones)
            
            # 6. Análisis de riesgos
            riesgos = self._analizar_riesgos(proyecto_data, metricas)
            
            # 7. Estructura completa del informe
            informe_completo = {
                # Datos básicos del proyecto
                "proyecto": {
                    "id": proyecto_data.get('id'),
                    "nombre": proyecto_data.get('nombre', 'Proyecto Sin Nombre'),
                    "cliente": proyecto_data.get('cliente', 'N/A'),
                    "descripcion": proyecto_data.get('descripcion', ''),
                    "estado": proyecto_data.get('estado', 'planificacion'),
                    "fecha_inicio": self._formatear_fecha(proyecto_data.get('fecha_inicio')),
                    "fecha_fin": self._formatear_fecha(proyecto_data.get('fecha_fin')) or 'En curso',
                    "duracion_dias": self._calcular_duracion(
                        proyecto_data.get('fecha_inicio'),
                        proyecto_data.get('fecha_fin')
                    )
                },
                
                # Resumen ejecutivo (lo más importante primero)
                "resumen_ejecutivo": {
                    "estado_general": analisis_estado.get('estado_general'),
                    "salud_financiera": analisis_estado.get('salud_financiera'),
                    "avance_porcentual": metricas.get('avance_porcentual', 0),
                    "mensaje_clave": analisis_estado.get('mensaje_clave'),
                    "puntos_destacados": analisis_estado.get('puntos_destacados', [])
                },
                
                # Métricas y KPIs
                "metricas": metricas,
                
                # Análisis financiero
                "financiero": {
                    "total_cotizaciones": metricas.get('total_cotizaciones', 0),
                    "cotizaciones_aprobadas": metricas.get('cotizaciones_aprobadas', 0),
                    "cotizaciones_pendientes": metricas.get('cotizaciones_pendientes', 0),
                    "cotizaciones_rechazadas": metricas.get('cotizaciones_rechazadas', 0),
                    "valor_total_cotizado": metricas.get('valor_total_cotizado', 0),
                    "valor_aprobado": metricas.get('valor_aprobado', 0),
                    "valor_pendiente": metricas.get('valor_pendiente', 0),
                    "tasa_aprobacion": metricas.get('tasa_aprobacion', 0),
                    "ticket_promedio": metricas.get('ticket_promedio', 0)
                },
                
                # Cotizaciones detalladas
                "cotizaciones": cotizaciones,
                
                # Documentos del proyecto
                "documentos": documentos,
                "total_documentos": len(documentos),
                
                # Timeline del proyecto
                "timeline": timeline,
                
                # Análisis de riesgos
                "riesgos": riesgos,
                
                # Conclusiones generadas por IA
                "conclusiones": conclusiones,
                
                # Recomendaciones
                "recomendaciones": recomendaciones,
                
                # Próximos pasos sugeridos
                "proximos_pasos": self._generar_proximos_pasos(proyecto_data, metricas),
                
                # Metadata del informe
                "metadata_informe": {
                    "fecha_generacion": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "version": "1.0",
                    "generado_por": "Tesla Cotizador v3.0",
                    "tipo": "Informe Ejecutivo Completo"
                }
            }
            
            logger.info("✅ Informe ejecutivo generado con análisis completo")
            
            return informe_completo
            
        except Exception as e:
            logger.error(f"Error al generar informe ejecutivo: {str(e)}")
            raise Exception(f"Error al generar informe: {str(e)}")
    
    # ════════════════════════════════════════════════════════
    # CÁLCULO DE MÉTRICAS Y KPIs
    # ════════════════════════════════════════════════════════
    
    def _calcular_metricas_proyecto(
        self,
        proyecto: Dict,
        cotizaciones: List[Dict],
        documentos: List[Dict]
    ) -> Dict[str, Any]:
        """
        Calcular todas las métricas del proyecto
        
        Returns:
            Dict con métricas calculadas
        """
        
        # Contadores básicos
        total_cot = len(cotizaciones)
        aprobadas = sum(1 for c in cotizaciones if c.get('estado') == 'aprobada')
        pendientes = sum(1 for c in cotizaciones if c.get('estado') == 'pendiente')
        rechazadas = sum(1 for c in cotizaciones if c.get('estado') == 'rechazada')
        
        # Valores financieros
        valor_total_cotizado = sum(float(c.get('total', 0)) for c in cotizaciones)
        valor_aprobado = sum(float(c.get('total', 0)) for c in cotizaciones if c.get('estado') == 'aprobada')
        valor_pendiente = sum(float(c.get('total', 0)) for c in cotizaciones if c.get('estado') == 'pendiente')
        
        # Tasas
        tasa_aprobacion = (aprobadas / total_cot * 100) if total_cot > 0 else 0
        tasa_conversion = tasa_aprobacion  # Alias
        
        # Ticket promedio
        ticket_promedio = (valor_aprobado / aprobadas) if aprobadas > 0 else 0
        
        # Avance del proyecto (estimación basada en cotizaciones aprobadas)
        avance_porcentual = min(tasa_aprobacion, 100)  # Simplificado
        
        # Documentos
        total_docs = len(documentos)
        docs_procesados = sum(1 for d in documentos if d.get('procesado') == 'Sí')
        
        # Tiempo
        duracion = self._calcular_duracion(
            proyecto.get('fecha_inicio'),
            proyecto.get('fecha_fin')
        )
        
        metricas = {
            # Cotizaciones
            "total_cotizaciones": total_cot,
            "cotizaciones_aprobadas": aprobadas,
            "cotizaciones_pendientes": pendientes,
            "cotizaciones_rechazadas": rechazadas,
            
            # Financiero
            "valor_total_cotizado": valor_total_cotizado,
            "valor_aprobado": valor_aprobado,
            "valor_pendiente": valor_pendiente,
            "subtotal": valor_aprobado,
            "igv": valor_aprobado * 0.18,
            "total": valor_aprobado * 1.18,
            
            # Tasas
            "tasa_aprobacion": round(tasa_aprobacion, 2),
            "tasa_conversion": round(tasa_conversion, 2),
            "ticket_promedio": round(ticket_promedio, 2),
            
            # Avance
            "avance_porcentual": round(avance_porcentual, 2),
            
            # Documentos
            "total_documentos": total_docs,
            "documentos_procesados": docs_procesados,
            
            # Tiempo
            "duracion_dias": duracion,
            "duracion_meses": round(duracion / 30, 1) if duracion else 0
        }
        
        return metricas
    
    # ════════════════════════════════════════════════════════
    # ANÁLISIS INTELIGENTE DEL ESTADO
    # ════════════════════════════════════════════════════════
    
    def _analizar_estado_proyecto(
        self,
        proyecto: Dict,
        metricas: Dict
    ) -> Dict[str, Any]:
        """
        Analizar el estado general del proyecto
        
        Returns:
            Dict con análisis del estado
        """
        
        estado = proyecto.get('estado', 'planificacion')
        tasa_aprobacion = metricas.get('tasa_aprobacion', 0)
        valor_aprobado = metricas.get('valor_aprobado', 0)
        
        # Estado general
        if estado == 'completado':
            estado_general = "COMPLETADO"
            color = "verde"
        elif estado == 'cancelado':
            estado_general = "CANCELADO"
            color = "rojo"
        elif estado == 'en_ejecucion':
            if tasa_aprobacion >= 70:
                estado_general = "EN BUEN CURSO"
                color = "verde"
            elif tasa_aprobacion >= 40:
                estado_general = "EN PROGRESO NORMAL"
                color = "amarillo"
            else:
                estado_general = "REQUIERE ATENCIÓN"
                color = "naranja"
        else:  # planificacion
            estado_general = "EN PLANIFICACIÓN"
            color = "azul"
        
        # Salud financiera
        if valor_aprobado >= 100000:
            salud_financiera = "EXCELENTE"
        elif valor_aprobado >= 50000:
            salud_financiera = "BUENA"
        elif valor_aprobado >= 10000:
            salud_financiera = "MODERADA"
        else:
            salud_financiera = "INICIAL"
        
        # Mensaje clave
        if tasa_aprobacion >= 80:
            mensaje_clave = f"Proyecto con alto índice de aprobación ({tasa_aprobacion:.0f}%). Excelente desempeño."
        elif tasa_aprobacion >= 50:
            mensaje_clave = f"Proyecto en desarrollo normal con {tasa_aprobacion:.0f}% de aprobación."
        else:
            mensaje_clave = f"Proyecto requiere atención. Solo {tasa_aprobacion:.0f}% de cotizaciones aprobadas."
        
        # Puntos destacados
        puntos = []
        
        if metricas.get('total_cotizaciones', 0) > 10:
            puntos.append(f"✓ Alto volumen de cotizaciones ({metricas['total_cotizaciones']})")
        
        if valor_aprobado > 50000:
            puntos.append(f"✓ Valor significativo aprobado (S/ {valor_aprobado:,.2f})")
        
        if tasa_aprobacion >= 70:
            puntos.append(f"✓ Excelente tasa de aprobación ({tasa_aprobacion:.0f}%)")
        
        if metricas.get('total_documentos', 0) > 5:
            puntos.append(f"✓ Documentación completa ({metricas['total_documentos']} archivos)")
        
        return {
            "estado_general": estado_general,
            "color_estado": color,
            "salud_financiera": salud_financiera,
            "mensaje_clave": mensaje_clave,
            "puntos_destacados": puntos
        }
    
    # ════════════════════════════════════════════════════════
    # GENERACIÓN DE CONCLUSIONES CON IA
    # ════════════════════════════════════════════════════════
    
    def _generar_conclusiones_ia(
        self,
        proyecto: Dict,
        metricas: Dict,
        analisis: Dict
    ) -> str:
        """
        Generar conclusiones inteligentes usando análisis de datos
        
        En producción, esto llamaría a Gemini.
        Por ahora, genera conclusiones basadas en reglas.
        
        Returns:
            Texto de conclusiones
        """
        
        conclusiones = []
        
        # Introducción
        conclusiones.append(
            f"El proyecto '{proyecto.get('nombre')}' para el cliente "
            f"{proyecto.get('cliente')} se encuentra actualmente en estado "
            f"{analisis.get('estado_general').lower()}."
        )
        
        # Análisis financiero
        valor_aprobado = metricas.get('valor_aprobado', 0)
        tasa_aprobacion = metricas.get('tasa_aprobacion', 0)
        
        if valor_aprobado > 0:
            conclusiones.append(
                f"Se ha logrado aprobar un monto de S/ {valor_aprobado:,.2f}, "
                f"representando una tasa de aprobación del {tasa_aprobacion:.1f}% "
                f"sobre el total cotizado."
            )
        
        # Análisis de desempeño
        if tasa_aprobacion >= 70:
            conclusiones.append(
                "El desempeño del proyecto es sobresaliente, superando las "
                "expectativas con una alta tasa de conversión de cotizaciones."
            )
        elif tasa_aprobacion >= 40:
            conclusiones.append(
                "El proyecto mantiene un desempeño aceptable, con espacio "
                "para optimización en la tasa de conversión."
            )
        else:
            conclusiones.append(
                "Se identifica oportunidad de mejora en la tasa de conversión "
                "de cotizaciones, lo cual requiere atención y análisis de causas."
            )
        
        # Documentación
        if metricas.get('total_documentos', 0) > 0:
            conclusiones.append(
                f"El proyecto cuenta con {metricas['total_documentos']} documentos "
                "de respaldo, evidenciando un adecuado nivel de documentación."
            )
        
        # Conclusión final
        if analisis.get('estado_general') in ['EN BUEN CURSO', 'COMPLETADO']:
            conclusiones.append(
                "En resumen, el proyecto presenta indicadores positivos y "
                "se recomienda continuar con la estrategia actual, "
                "manteniendo el seguimiento de los hitos establecidos."
            )
        else:
            conclusiones.append(
                "Se recomienda implementar las acciones correctivas sugeridas "
                "para mejorar los indicadores del proyecto y asegurar el "
                "cumplimiento de objetivos."
            )
        
        return " ".join(conclusiones)
    
    # ════════════════════════════════════════════════════════
    # GENERACIÓN DE RECOMENDACIONES
    # ════════════════════════════════════════════════════════
    
    def _generar_recomendaciones(
        self,
        proyecto: Dict,
        metricas: Dict,
        analisis: Dict
    ) -> List[str]:
        """
        Generar recomendaciones basadas en el análisis
        
        Returns:
            Lista de recomendaciones
        """
        
        recomendaciones = []
        
        tasa_aprobacion = metricas.get('tasa_aprobacion', 0)
        pendientes = metricas.get('cotizaciones_pendientes', 0)
        
        # Recomendación por tasa de aprobación
        if tasa_aprobacion < 50:
            recomendaciones.append(
                "🔍 Analizar las causas de rechazo de cotizaciones y ajustar "
                "la estrategia de precios o alcances."
            )
        
        # Recomendación por cotizaciones pendientes
        if pendientes > 3:
            recomendaciones.append(
                f"⏱️ Hacer seguimiento a las {pendientes} cotizaciones pendientes "
                "para acelerar el proceso de aprobación."
            )
        
        # Recomendación por documentación
        if metricas.get('total_documentos', 0) < 3:
            recomendaciones.append(
                "📄 Incrementar la documentación del proyecto para mejor "
                "trazabilidad y respaldo."
            )
        
        # Recomendación por valor
        if metricas.get('valor_aprobado', 0) > 100000:
            recomendaciones.append(
                "💰 Considerar segmentación del proyecto en fases para "
                "optimizar el flujo de caja y reducir riesgos."
            )
        
        # Recomendación general
        recomendaciones.append(
            "📊 Mantener reuniones semanales de seguimiento con el cliente "
            "para asegurar alineación de expectativas."
        )
        
        recomendaciones.append(
            "✅ Documentar lecciones aprendidas para mejorar futuros proyectos."
        )
        
        return recomendaciones
    
    # ════════════════════════════════════════════════════════
    # GENERACIÓN DE TIMELINE
    # ════════════════════════════════════════════════════════
    
    def _generar_timeline(
        self,
        proyecto: Dict,
        cotizaciones: List[Dict]
    ) -> List[Dict[str, str]]:
        """
        Generar timeline del proyecto
        
        Returns:
            Lista de eventos del timeline
        """
        
        timeline = []
        
        # Evento: Inicio del proyecto
        if proyecto.get('fecha_inicio'):
            timeline.append({
                "fecha": self._formatear_fecha(proyecto['fecha_inicio']),
                "evento": "Inicio del Proyecto",
                "descripcion": f"Proyecto '{proyecto.get('nombre')}' iniciado"
            })
        
        # Eventos: Cotizaciones aprobadas (máximo 5 más recientes)
        cot_aprobadas = [
            c for c in cotizaciones 
            if c.get('estado') == 'aprobada'
        ]
        
        for cot in sorted(cot_aprobadas, key=lambda x: x.get('fecha_creacion', ''), reverse=True)[:5]:
            timeline.append({
                "fecha": cot.get('fecha_creacion', 'N/A'),
                "evento": f"Cotización {cot.get('numero')} Aprobada",
                "descripcion": f"Monto: S/ {float(cot.get('total', 0)):,.2f}"
            })
        
        # Evento: Fin del proyecto (si existe)
        if proyecto.get('fecha_fin'):
            timeline.append({
                "fecha": self._formatear_fecha(proyecto['fecha_fin']),
                "evento": "Finalización del Proyecto",
                "descripcion": f"Proyecto completado"
            })
        
        # Ordenar por fecha
        timeline.sort(key=lambda x: x['fecha'])
        
        return timeline
    
    # ════════════════════════════════════════════════════════
    # ANÁLISIS DE RIESGOS
    # ════════════════════════════════════════════════════════
    
    def _analizar_riesgos(
        self,
        proyecto: Dict,
        metricas: Dict
    ) -> List[Dict[str, str]]:
        """
        Identificar riesgos del proyecto
        
        Returns:
            Lista de riesgos identificados
        """
        
        riesgos = []
        
        # Riesgo: Baja tasa de aprobación
        if metricas.get('tasa_aprobacion', 0) < 40:
            riesgos.append({
                "nivel": "ALTO",
                "tipo": "Comercial",
                "descripcion": "Tasa de aprobación baja puede afectar la viabilidad del proyecto",
                "mitigacion": "Revisar precios y propuesta de valor con el cliente"
            })
        
        # Riesgo: Muchas cotizaciones pendientes
        if metricas.get('cotizaciones_pendientes', 0) > 5:
            riesgos.append({
                "nivel": "MEDIO",
                "tipo": "Operativo",
                "descripcion": "Acumulación de cotizaciones pendientes",
                "mitigacion": "Intensificar seguimiento comercial"
            })
        
        # Riesgo: Poca documentación
        if metricas.get('total_documentos', 0) < 2:
            riesgos.append({
                "nivel": "MEDIO",
                "tipo": "Documentación",
                "descripcion": "Documentación insuficiente del proyecto",
                "mitigacion": "Solicitar y almacenar documentos clave del proyecto"
            })
        
        # Riesgo: Proyecto sin fecha de fin
        if not proyecto.get('fecha_fin') and proyecto.get('estado') == 'en_ejecucion':
            riesgos.append({
                "nivel": "BAJO",
                "tipo": "Planificación",
                "descripcion": "Proyecto sin fecha de cierre definida",
                "mitigacion": "Establecer timeline y milestones con el cliente"
            })
        
        # Si no hay riesgos, agregar mensaje positivo
        if not riesgos:
            riesgos.append({
                "nivel": "NINGUNO",
                "tipo": "General",
                "descripcion": "No se identifican riesgos significativos en este momento",
                "mitigacion": "Continuar con monitoreo regular"
            })
        
        return riesgos
    
    # ════════════════════════════════════════════════════════
    # PRÓXIMOS PASOS
    # ════════════════════════════════════════════════════════
    
    def _generar_proximos_pasos(
        self,
        proyecto: Dict,
        metricas: Dict
    ) -> List[str]:
        """
        Generar lista de próximos pasos sugeridos
        
        Returns:
            Lista de acciones sugeridas
        """
        
        pasos = []
        
        estado = proyecto.get('estado', 'planificacion')
        pendientes = metricas.get('cotizaciones_pendientes', 0)
        
        if estado == 'planificacion':
            pasos.append("1. Finalizar alcance del proyecto con el cliente")
            pasos.append("2. Generar cotización formal")
            pasos.append("3. Programar reunión de presentación")
        
        elif estado == 'en_ejecucion':
            if pendientes > 0:
                pasos.append(f"1. Hacer seguimiento a {pendientes} cotizaciones pendientes")
            
            pasos.append("2. Actualizar cronograma del proyecto")
            pasos.append("3. Preparar reporte de avance para el cliente")
            pasos.append("4. Revisar hitos y entregas próximas")
        
        elif estado == 'completado':
            pasos.append("1. Solicitar feedback del cliente")
            pasos.append("2. Documentar lecciones aprendidas")
            pasos.append("3. Archivar documentación del proyecto")
        
        else:
            pasos.append("1. Definir próximas acciones con el equipo")
            pasos.append("2. Actualizar estado del proyecto")
        
        return pasos
    
    # ════════════════════════════════════════════════════════
    # UTILIDADES
    # ════════════════════════════════════════════════════════
    
    def _formatear_fecha(self, fecha) -> Optional[str]:
        """Formatear fecha a string"""
        if not fecha:
            return None
        
        if isinstance(fecha, str):
            return fecha
        
        try:
            return fecha.strftime('%d/%m/%Y')
        except:
            return str(fecha)
    
    def _calcular_duracion(self, fecha_inicio, fecha_fin) -> int:
        """
        Calcular duración en días
        
        Returns:
            Número de días
        """
        if not fecha_inicio:
            return 0
        
        try:
            if isinstance(fecha_inicio, str):
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            
            if fecha_fin:
                if isinstance(fecha_fin, str):
                    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            else:
                fecha_fin = datetime.now()
            
            delta = fecha_fin - fecha_inicio
            return delta.days
            
        except:
            return 0

# ════════════════════════════════════════════════════════
# INSTANCIA GLOBAL
# ════════════════════════════════════════════════════════

report_generator = ReportGenerator()