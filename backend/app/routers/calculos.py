from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import math

router = APIRouter(tags=["Calculos Deterministicos"])

# ==========================================
# MODELOS
# ==========================================

class CronogramaInput(BaseModel):
    duracion_total: int
    fecha_inicio: str  # Format: YYYY-MM-DD or DD/MM/YYYY
    incluir_fines_semana: bool = True

class FaseOutput(BaseModel):
    id: int
    nombre: str
    duracion_dias: int
    fecha_inicio: str
    fecha_fin: str
    porcentaje: int
    color: str

class CronogramaOutput(BaseModel):
    duracion_total_calculada: int
    fecha_inicio: str
    fecha_fin_estimada: str
    fases: List[FaseOutput]

# ==========================================
# LÓGICA DE NEGOCIO
# ==========================================

@router.post("/cronograma-pmi", response_model=CronogramaOutput)
async def calcular_cronograma_pmi(datos: CronogramaInput = Body(...)):
    """
    Calcula un cronograma PMI determinístico basado en la duración total.
    Distribución estándar:
    1. Iniciación: 5%
    2. Planificación: 15%
    3. Ejecución: 40%
    4. Monitoreo y Control: 30%
    5. Cierre: 10%
    """
    try:
        # 1. Normalizar fecha
        fecha_str = datos.fecha_inicio
        try:
            if "/" in fecha_str:
                fecha_obj = datetime.strptime(fecha_str, "%d/%m/%Y")
            else:
                fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d")
        except ValueError:
            # Fallback a hoy si falla
            fecha_obj = datetime.now()
        
        total_dias = max(datos.duracion_total, 5) # Mínimo 5 días

        # 2. Definir Distribución (Porcentajes)
        # Ajustado para que sume 100% y tenga sentido constructivo
        estructura_fases = [
            {"nombre": "1. Iniciación (Acta de Constitución)", "pct": 5, "color": "#64748b"},
            {"nombre": "2. Planificación (Alcance y Cronograma)", "pct": 15, "color": "#0ea5e9"},
            {"nombre": "3. Ejecución (Implementación Eléctrica)", "pct": 45, "color": "#22c55e"},
            {"nombre": "4. Monitoreo y Control (Calidad)", "pct": 25, "color": "#eab308"},
            {"nombre": "5. Cierre (Entrega y Dossier)", "pct": 10, "color": "#ef4444"}
        ]

        fases_calculadas = []
        dias_acumulados = 0
        current_date = fecha_obj
        
        # 3. Calcular días por fase
        total_dias_asignados = 0
        
        for i, fase in enumerate(estructura_fases):
            if i == len(estructura_fases) - 1:
                # Última fase toma el remanente para cuadrar exacto
                dias_fase = total_dias - total_dias_asignados
            else:
                dias_fase = math.floor(total_dias * (fase["pct"] / 100))
                if dias_fase < 1: dias_fase = 1 # Mínimo 1 día por fase
            
            total_dias_asignados += dias_fase
            
            # Calcular fechas fase
            f_inicio = current_date
            f_fin = current_date + timedelta(days=dias_fase)
            
            fases_calculadas.append({
                "id": i + 1,
                "nombre": fase["nombre"],
                "duracion_dias": dias_fase,
                "fecha_inicio": f_inicio.strftime("%d/%m/%Y"),
                "fecha_fin": f_fin.strftime("%d/%m/%Y"),
                "porcentaje": fase["pct"],
                "color": fase["color"]
            })
            
            current_date = f_fin # Siguiente fase empieza donde termina esta

        return {
            "duracion_total_calculada": total_dias_asignados,
            "fecha_inicio": fecha_obj.strftime("%d/%m/%Y"),
            "fecha_fin_estimada": current_date.strftime("%d/%m/%Y"),
            "fases": fases_calculadas
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculando cronograma: {str(e)}")
