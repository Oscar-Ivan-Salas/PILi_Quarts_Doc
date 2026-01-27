"""
MOTOR DE GRAFICAS PROFESIONALES v4.0
Generacion de visualizaciones de clase mundial con Plotly

Tipos de graficas:
- Barras (costos, comparativas)
- Lineas (tendencias, proyecciones)
- Pie/Donut (distribuciones)
- Gantt (cronogramas de proyecto)
- Heatmaps (matrices de riesgo)
- KPI Dashboards
- Flujo de caja
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# Imports condicionales
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    logger.warning("plotly no disponible - pip install plotly")

try:
    import kaleido
    KALEIDO_AVAILABLE = True
except ImportError:
    KALEIDO_AVAILABLE = False
    logger.warning("kaleido no disponible - pip install kaleido")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False


class ChartEngine:
    """
    Motor de graficas profesionales para documentos.

    Genera visualizaciones de alta calidad que pueden
    exportarse a PNG/PDF para embeber en documentos Word.
    """

    def __init__(self, output_dir: str = None):
        """
        Inicializa el motor de graficas.

        Args:
            output_dir: Directorio para guardar imagenes
        """
        self.output_dir = Path(output_dir) if output_dir else Path("backend/storage/temp/charts")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Colores corporativos Tesla
        self.colors = {
            "primary": "#D4AF37",      # Dorado
            "secondary": "#8B0000",     # Rojo oscuro
            "accent": "#0066CC",        # Azul tech
            "success": "#28a745",       # Verde
            "warning": "#ffc107",       # Amarillo
            "danger": "#dc3545",        # Rojo
            "dark": "#333333",          # Gris oscuro
            "light": "#f8f9fa"          # Gris claro
        }

        # Paleta para graficas
        self.color_palette = [
            "#D4AF37", "#8B0000", "#0066CC", "#28a745",
            "#ffc107", "#6f42c1", "#17a2b8", "#fd7e14"
        ]

        logger.info(f"ChartEngine inicializado - Plotly: {PLOTLY_AVAILABLE}, Kaleido: {KALEIDO_AVAILABLE}")

    def is_available(self) -> bool:
        """Verifica si el motor esta disponible"""
        return PLOTLY_AVAILABLE

    # =========================================================================
    # GRAFICAS DE BARRAS
    # =========================================================================

    def create_bar_chart(
        self,
        data: Dict[str, float],
        title: str = "Grafico de Barras",
        x_label: str = "Categorias",
        y_label: str = "Valores",
        horizontal: bool = False,
        show_values: bool = True
    ) -> Optional[str]:
        """
        Crea grafico de barras.

        Args:
            data: Diccionario {categoria: valor}
            title: Titulo del grafico
            horizontal: Si es True, barras horizontales
            show_values: Mostrar valores sobre barras

        Returns:
            Ruta al archivo PNG generado
        """
        if not PLOTLY_AVAILABLE:
            return None

        categories = list(data.keys())
        values = list(data.values())

        if horizontal:
            fig = go.Figure(go.Bar(
                x=values,
                y=categories,
                orientation='h',
                marker_color=self.colors["primary"],
                text=values if show_values else None,
                textposition='outside'
            ))
            fig.update_layout(xaxis_title=y_label, yaxis_title=x_label)
        else:
            fig = go.Figure(go.Bar(
                x=categories,
                y=values,
                marker_color=self.colors["primary"],
                text=values if show_values else None,
                textposition='outside'
            ))
            fig.update_layout(xaxis_title=x_label, yaxis_title=y_label)

        fig.update_layout(
            title=title,
            template="plotly_white",
            font=dict(family="Arial", size=12)
        )

        return self._save_figure(fig, f"bar_{datetime.now().strftime('%Y%m%d%H%M%S')}")

    def create_grouped_bar_chart(
        self,
        data: Dict[str, Dict[str, float]],
        title: str = "Comparativa",
        x_label: str = "Categorias",
        y_label: str = "Valores"
    ) -> Optional[str]:
        """
        Crea grafico de barras agrupadas para comparativas.

        Args:
            data: {grupo: {categoria: valor}}

        Returns:
            Ruta al archivo PNG
        """
        if not PLOTLY_AVAILABLE:
            return None

        fig = go.Figure()

        for i, (group_name, group_data) in enumerate(data.items()):
            fig.add_trace(go.Bar(
                name=group_name,
                x=list(group_data.keys()),
                y=list(group_data.values()),
                marker_color=self.color_palette[i % len(self.color_palette)]
            ))

        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            barmode='group',
            template="plotly_white"
        )

        return self._save_figure(fig, f"grouped_bar_{datetime.now().strftime('%Y%m%d%H%M%S')}")

    # =========================================================================
    # GRAFICAS DE LINEAS
    # =========================================================================

    def create_line_chart(
        self,
        data: Dict[str, List[float]],
        x_values: List[str],
        title: str = "Tendencia",
        x_label: str = "Periodo",
        y_label: str = "Valor"
    ) -> Optional[str]:
        """
        Crea grafico de lineas para tendencias.

        Args:
            data: {serie: [valores]}
            x_values: Etiquetas eje X

        Returns:
            Ruta al archivo PNG
        """
        if not PLOTLY_AVAILABLE:
            return None

        fig = go.Figure()

        for i, (name, values) in enumerate(data.items()):
            fig.add_trace(go.Scatter(
                x=x_values,
                y=values,
                mode='lines+markers',
                name=name,
                line=dict(color=self.color_palette[i % len(self.color_palette)], width=2),
                marker=dict(size=8)
            ))

        fig.update_layout(
            title=title,
            xaxis_title=x_label,
            yaxis_title=y_label,
            template="plotly_white",
            hovermode='x unified'
        )

        return self._save_figure(fig, f"line_{datetime.now().strftime('%Y%m%d%H%M%S')}")

    def create_projection_chart(
        self,
        historical: List[float],
        projected: List[float],
        labels: List[str],
        title: str = "Proyeccion",
        y_label: str = "Valor"
    ) -> Optional[str]:
        """
        Crea grafico con datos historicos y proyectados.

        Returns:
            Ruta al archivo PNG
        """
        if not PLOTLY_AVAILABLE:
            return None

        fig = go.Figure()

        # Datos historicos
        fig.add_trace(go.Scatter(
            x=labels[:len(historical)],
            y=historical,
            mode='lines+markers',
            name='Historico',
            line=dict(color=self.colors["primary"], width=3),
            marker=dict(size=10)
        ))

        # Datos proyectados
        fig.add_trace(go.Scatter(
            x=labels[len(historical)-1:],
            y=[historical[-1]] + projected,
            mode='lines+markers',
            name='Proyectado',
            line=dict(color=self.colors["accent"], width=3, dash='dash'),
            marker=dict(size=10)
        ))

        fig.update_layout(
            title=title,
            yaxis_title=y_label,
            template="plotly_white"
        )

        return self._save_figure(fig, f"projection_{datetime.now().strftime('%Y%m%d%H%M%S')}")

    # =========================================================================
    # GRAFICAS CIRCULARES
    # =========================================================================

    def create_pie_chart(
        self,
        data: Dict[str, float],
        title: str = "Distribucion",
        hole: float = 0.3
    ) -> Optional[str]:
        """
        Crea grafico de pie/donut.

        Args:
            data: {categoria: valor}
            hole: 0 para pie, >0 para donut

        Returns:
            Ruta al archivo PNG
        """
        if not PLOTLY_AVAILABLE:
            return None

        labels = list(data.keys())
        values = list(data.values())

        fig = go.Figure(go.Pie(
            labels=labels,
            values=values,
            hole=hole,
            marker_colors=self.color_palette[:len(labels)],
            textinfo='percent+label',
            textposition='outside'
        ))

        fig.update_layout(
            title=title,
            template="plotly_white"
        )

        return self._save_figure(fig, f"pie_{datetime.now().strftime('%Y%m%d%H%M%S')}")

    # =========================================================================
    # DIAGRAMA GANTT
    # =========================================================================

    def create_gantt_chart(
        self,
        tasks: List[Dict[str, Any]],
        title: str = "Cronograma del Proyecto"
    ) -> Optional[str]:
        """
        Crea diagrama de Gantt profesional.

        Args:
            tasks: Lista de tareas con formato:
                   [{"nombre": "Tarea", "inicio": "2024-01-01", "fin": "2024-01-15", "progreso": 50}]

        Returns:
            Ruta al archivo PNG
        """
        if not PLOTLY_AVAILABLE or not PANDAS_AVAILABLE:
            return None

        # Convertir a DataFrame
        df_data = []
        for i, task in enumerate(tasks):
            df_data.append({
                "Task": task.get("nombre", f"Tarea {i+1}"),
                "Start": task.get("inicio", task.get("fecha_inicio")),
                "Finish": task.get("fin", task.get("fecha_fin")),
                "Resource": task.get("recurso", "General"),
                "Progress": task.get("progreso", 0)
            })

        df = pd.DataFrame(df_data)

        # Crear Gantt
        fig = px.timeline(
            df,
            x_start="Start",
            x_end="Finish",
            y="Task",
            color="Resource",
            title=title,
            color_discrete_sequence=self.color_palette
        )

        fig.update_yaxes(autorange="reversed")
        fig.update_layout(
            template="plotly_white",
            xaxis_title="Fecha",
            yaxis_title="Fase/Tarea"
        )

        return self._save_figure(fig, f"gantt_{datetime.now().strftime('%Y%m%d%H%M%S')}")

    # =========================================================================
    # HEATMAP / MATRIZ DE RIESGOS
    # =========================================================================

    def create_risk_matrix(
        self,
        risks: List[Dict[str, Any]],
        title: str = "Matriz de Riesgos"
    ) -> Optional[str]:
        """
        Crea matriz de riesgos probabilidad/impacto.

        Args:
            risks: Lista con formato:
                   [{"nombre": "Riesgo", "probabilidad": 3, "impacto": 4}]
                   Donde valores van de 1 (bajo) a 5 (alto)

        Returns:
            Ruta al archivo PNG
        """
        if not PLOTLY_AVAILABLE:
            return None

        # Crear matriz 5x5
        matrix = [[0]*5 for _ in range(5)]

        # Colocar riesgos en matriz
        risk_labels = []
        for risk in risks:
            prob = min(5, max(1, risk.get("probabilidad", 3))) - 1
            imp = min(5, max(1, risk.get("impacto", 3))) - 1
            matrix[prob][imp] += 1
            risk_labels.append(risk.get("nombre", "Riesgo"))

        # Colores: verde (bajo) -> amarillo -> rojo (alto)
        colorscale = [
            [0, "#28a745"],
            [0.25, "#7cb342"],
            [0.5, "#ffc107"],
            [0.75, "#ff9800"],
            [1, "#dc3545"]
        ]

        fig = go.Figure(go.Heatmap(
            z=matrix,
            x=["Muy Bajo", "Bajo", "Medio", "Alto", "Muy Alto"],
            y=["Muy Baja", "Baja", "Media", "Alta", "Muy Alta"],
            colorscale=colorscale,
            showscale=False,
            text=matrix,
            texttemplate="%{text}",
            textfont={"size": 14}
        ))

        fig.update_layout(
            title=title,
            xaxis_title="Impacto",
            yaxis_title="Probabilidad",
            template="plotly_white"
        )

        return self._save_figure(fig, f"risk_matrix_{datetime.now().strftime('%Y%m%d%H%M%S')}")

    # =========================================================================
    # KPI DASHBOARD
    # =========================================================================

    def create_kpi_dashboard(
        self,
        kpis: Dict[str, Dict[str, Any]],
        title: str = "Dashboard de KPIs"
    ) -> Optional[str]:
        """
        Crea dashboard con indicadores KPI.

        Args:
            kpis: {nombre: {"valor": 95, "meta": 100, "unidad": "%"}}

        Returns:
            Ruta al archivo PNG
        """
        if not PLOTLY_AVAILABLE:
            return None

        n_kpis = len(kpis)
        cols = min(3, n_kpis)
        rows = (n_kpis + cols - 1) // cols

        fig = make_subplots(
            rows=rows,
            cols=cols,
            specs=[[{"type": "indicator"}] * cols for _ in range(rows)],
            vertical_spacing=0.3
        )

        for i, (name, data) in enumerate(kpis.items()):
            row = i // cols + 1
            col = i % cols + 1

            valor = data.get("valor", 0)
            meta = data.get("meta", 100)
            unidad = data.get("unidad", "")

            # Color segun cumplimiento
            ratio = valor / meta if meta > 0 else 0
            color = self.colors["success"] if ratio >= 1 else \
                   self.colors["warning"] if ratio >= 0.8 else \
                   self.colors["danger"]

            fig.add_trace(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=valor,
                    delta={"reference": meta, "relative": True},
                    title={"text": name},
                    number={"suffix": unidad},
                    gauge={
                        "axis": {"range": [0, meta * 1.2]},
                        "bar": {"color": color},
                        "threshold": {
                            "line": {"color": self.colors["dark"], "width": 2},
                            "thickness": 0.75,
                            "value": meta
                        }
                    }
                ),
                row=row, col=col
            )

        fig.update_layout(
            title=title,
            template="plotly_white",
            height=300 * rows
        )

        return self._save_figure(fig, f"kpi_dashboard_{datetime.now().strftime('%Y%m%d%H%M%S')}")

    # =========================================================================
    # FLUJO DE CAJA
    # =========================================================================

    def create_cashflow_chart(
        self,
        inflows: List[float],
        outflows: List[float],
        periods: List[str],
        title: str = "Flujo de Caja"
    ) -> Optional[str]:
        """
        Crea grafico de flujo de caja.

        Args:
            inflows: Ingresos por periodo
            outflows: Egresos por periodo
            periods: Etiquetas de periodos

        Returns:
            Ruta al archivo PNG
        """
        if not PLOTLY_AVAILABLE:
            return None

        # Calcular flujo neto acumulado
        net_flow = [i - o for i, o in zip(inflows, outflows)]
        cumulative = []
        total = 0
        for nf in net_flow:
            total += nf
            cumulative.append(total)

        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Barras de ingresos
        fig.add_trace(
            go.Bar(name="Ingresos", x=periods, y=inflows,
                   marker_color=self.colors["success"]),
            secondary_y=False
        )

        # Barras de egresos (negativos)
        fig.add_trace(
            go.Bar(name="Egresos", x=periods, y=[-o for o in outflows],
                   marker_color=self.colors["danger"]),
            secondary_y=False
        )

        # Linea de acumulado
        fig.add_trace(
            go.Scatter(name="Acumulado", x=periods, y=cumulative,
                      mode='lines+markers',
                      line=dict(color=self.colors["primary"], width=3)),
            secondary_y=True
        )

        fig.update_layout(
            title=title,
            template="plotly_white",
            barmode='relative',
            hovermode='x unified'
        )

        fig.update_yaxes(title_text="Flujo de Caja", secondary_y=False)
        fig.update_yaxes(title_text="Acumulado", secondary_y=True)

        return self._save_figure(fig, f"cashflow_{datetime.now().strftime('%Y%m%d%H%M%S')}")

    # =========================================================================
    # METODOS AUXILIARES
    # =========================================================================

    def _save_figure(self, fig, filename: str) -> Optional[str]:
        """Guarda figura como PNG"""
        try:
            filepath = self.output_dir / f"{filename}.png"

            if KALEIDO_AVAILABLE:
                fig.write_image(str(filepath), width=800, height=600, scale=2)
            else:
                # Fallback: guardar como HTML
                filepath = self.output_dir / f"{filename}.html"
                fig.write_html(str(filepath))

            logger.info(f"Grafica guardada: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Error guardando grafica: {e}")
            return None

    def create_charts_for_document(
        self,
        document_type: str,
        data: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Genera todas las graficas necesarias para un tipo de documento.

        Args:
            document_type: "cotizacion", "proyecto", "informe"
            data: Datos del documento

        Returns:
            Dict con rutas a las graficas generadas
        """
        charts = {}

        if document_type == "proyecto":
            # Gantt de fases
            if "fases" in data:
                tasks = []
                fecha_actual = datetime.now()
                for fase in data["fases"]:
                    fecha_fin = fecha_actual + timedelta(days=fase.get("duracion_dias", 7))
                    tasks.append({
                        "nombre": fase.get("nombre"),
                        "inicio": fecha_actual.strftime("%Y-%m-%d"),
                        "fin": fecha_fin.strftime("%Y-%m-%d"),
                        "progreso": fase.get("progreso", 0)
                    })
                    fecha_actual = fecha_fin

                charts["gantt"] = self.create_gantt_chart(tasks)

            # Matriz de riesgos
            if "riesgos" in data:
                risks = []
                for r in data["riesgos"]:
                    prob = 3 if r.get("probabilidad") == "Media" else \
                           4 if r.get("probabilidad") == "Alta" else 2
                    imp = 4 if r.get("impacto") == "Alto" else \
                          3 if r.get("impacto") == "Medio" else 2
                    risks.append({
                        "nombre": r.get("riesgo"),
                        "probabilidad": prob,
                        "impacto": imp
                    })
                charts["risk_matrix"] = self.create_risk_matrix(risks)

        elif document_type == "informe":
            # KPIs
            if "metricas_clave" in data:
                kpis = {}
                metricas = data["metricas_clave"]
                if "roi_estimado" in metricas:
                    kpis["ROI"] = {"valor": metricas["roi_estimado"], "meta": 20, "unidad": "%"}
                if "reduccion_costos_operativos" in metricas:
                    kpis["Reduccion Costos"] = {"valor": metricas["reduccion_costos_operativos"], "meta": 15, "unidad": "%"}

                if kpis:
                    charts["kpis"] = self.create_kpi_dashboard(kpis)

        elif document_type == "cotizacion":
            # Distribucion de costos
            if "items" in data:
                costs = {}
                for item in data["items"]:
                    desc = item.get("descripcion", "Item")[:20]
                    costs[desc] = item.get("total", 0)

                if costs:
                    charts["cost_distribution"] = self.create_pie_chart(
                        costs, "Distribucion de Costos"
                    )

        return charts


# Instancia global
chart_engine = ChartEngine()

def get_chart_engine() -> ChartEngine:
    """Obtiene la instancia del motor de graficas"""
    return chart_engine
