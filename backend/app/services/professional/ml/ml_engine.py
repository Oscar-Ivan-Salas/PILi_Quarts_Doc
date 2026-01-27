"""
MOTOR DE MACHINE LEARNING LOCAL v4.0
NLP y clasificacion sin necesidad de IA en red

Componentes:
- spaCy para NER (Named Entity Recognition)
- Clasificadores sklearn para deteccion de servicios
- Extraccion de entidades (areas, cantidades, precios)
- Analisis de sentimiento basico
"""

import re
import logging
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import json

logger = logging.getLogger(__name__)

# Imports condicionales
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    logger.warning("spaCy no disponible - pip install spacy")

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import Pipeline
    import joblib
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning("sklearn no disponible - pip install scikit-learn")

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


class MLEngine:
    """
    Motor de Machine Learning local para PILI.

    Proporciona:
    - Clasificacion de servicios
    - Extraccion de entidades (NER)
    - Analisis de texto
    - Todo funciona 100% offline
    """

    def __init__(self, models_dir: str = None):
        """
        Inicializa el motor ML.

        Args:
            models_dir: Directorio para modelos entrenados
        """
        self.models_dir = Path(models_dir) if models_dir else Path("backend/ml_models")
        self.models_dir.mkdir(parents=True, exist_ok=True)

        self.nlp = None
        self.classifier = None

        # Datos de entrenamiento para clasificador de servicios
        self.service_training_data = self._get_training_data()

        # Patrones para extraccion de entidades
        self.patterns = {
            "area": [
                r"(\d+(?:\.\d+)?)\s*(?:m2|metros cuadrados|m²)",
                r"area\s*(?:de)?\s*(\d+(?:\.\d+)?)",
                r"(\d+(?:\.\d+)?)\s*metros"
            ],
            "cantidad": [
                r"(\d+)\s*(?:puntos|circuitos|tomacorrientes|luminarias)",
                r"cantidad\s*(?:de)?\s*(\d+)",
                r"(\d+)\s*unidades"
            ],
            "precio": [
                r"(?:S/\.?|PEN|soles?)\s*(\d+(?:,\d{3})*(?:\.\d{2})?)",
                r"(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:soles?|S/\.?)",
                r"\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)"
            ],
            "pisos": [
                r"(\d+)\s*(?:pisos?|niveles?|plantas?)",
                r"(?:edificio|casa)\s*(?:de)?\s*(\d+)\s*pisos?"
            ],
            "potencia": [
                r"(\d+(?:\.\d+)?)\s*(?:kw|kilowatts?|kva)",
                r"potencia\s*(?:de)?\s*(\d+(?:\.\d+)?)"
            ]
        }

        # Inicializar componentes
        self._initialize_components()

        logger.info("MLEngine inicializado")

    def _initialize_components(self):
        """Inicializa spaCy y clasificador"""

        # Inicializar spaCy
        if SPACY_AVAILABLE:
            try:
                # Intentar cargar modelo en español
                self.nlp = spacy.load("es_core_news_sm")
                logger.info("spaCy modelo español cargado")
            except OSError:
                try:
                    # Fallback a modelo multilingue
                    self.nlp = spacy.load("xx_ent_wiki_sm")
                    logger.info("spaCy modelo multilingue cargado")
                except OSError:
                    logger.warning("No hay modelos spaCy disponibles - ejecutar: python -m spacy download es_core_news_sm")
                    self.nlp = None

        # Inicializar clasificador
        if SKLEARN_AVAILABLE:
            self._train_classifier()

    def _get_training_data(self) -> Dict[str, List[str]]:
        """Datos de entrenamiento para clasificador de servicios"""

        return {
            "electrico-residencial": [
                "instalacion electrica para casa",
                "cableado residencial",
                "puntos de luz para vivienda",
                "tablero electrico domiciliario",
                "tomacorrientes para casa",
                "iluminacion residencial",
                "circuitos electricos casa",
                "conexion electrica domiciliaria"
            ],
            "electrico-comercial": [
                "instalacion electrica comercial",
                "local comercial electrico",
                "tienda electricidad",
                "oficina instalacion electrica",
                "tablero comercial",
                "iluminacion comercial",
                "cableado para negocio"
            ],
            "electrico-industrial": [
                "instalacion industrial electrica",
                "planta industrial",
                "fabrica electricidad",
                "media tension",
                "subestacion electrica",
                "tablero industrial",
                "motor electrico",
                "potencia industrial"
            ],
            "contraincendios": [
                "sistema contra incendios",
                "alarma incendio",
                "detector humo",
                "rociadores",
                "extintor",
                "gabinete incendio",
                "bomba contra incendio",
                "nfpa"
            ],
            "domotica": [
                "domotica",
                "casa inteligente",
                "smart home",
                "automatizacion hogar",
                "control luces",
                "sensor movimiento",
                "alexa",
                "google home"
            ],
            "expedientes": [
                "expediente tecnico",
                "planos arquitectura",
                "memoria descriptiva",
                "licencia construccion",
                "municipalidad",
                "permiso obra",
                "conformidad"
            ],
            "saneamiento": [
                "agua potable",
                "desague",
                "sanitario",
                "tuberia agua",
                "cisterna",
                "tanque elevado",
                "bomba agua"
            ],
            "itse": [
                "certificado itse",
                "inspeccion tecnica",
                "seguridad edificaciones",
                "defensa civil",
                "indeci",
                "seguridad local"
            ],
            "pozo-tierra": [
                "pozo a tierra",
                "puesta a tierra",
                "electrodo tierra",
                "resistividad",
                "ohms tierra",
                "pararrayo"
            ],
            "redes-cctv": [
                "camaras seguridad",
                "cctv",
                "videovigilancia",
                "red datos",
                "cableado estructurado",
                "rack",
                "switch red"
            ]
        }

    def _train_classifier(self):
        """Entrena el clasificador de servicios"""

        if not SKLEARN_AVAILABLE:
            return

        # Preparar datos
        texts = []
        labels = []

        for service, examples in self.service_training_data.items():
            for text in examples:
                texts.append(text)
                labels.append(service)

        # Crear pipeline
        self.classifier = Pipeline([
            ('tfidf', TfidfVectorizer(
                ngram_range=(1, 2),
                max_features=1000,
                stop_words=None  # Mantener palabras en español
            )),
            ('clf', MultinomialNB(alpha=0.1))
        ])

        # Entrenar
        self.classifier.fit(texts, labels)
        logger.info(f"Clasificador entrenado con {len(texts)} ejemplos")

    def classify_service(self, text: str) -> Dict[str, Any]:
        """
        Clasifica el servicio mencionado en el texto.

        Args:
            text: Texto a clasificar

        Returns:
            Dict con servicio detectado y confianza
        """
        text_lower = text.lower()

        # Usar clasificador ML si esta disponible
        if self.classifier:
            try:
                service = self.classifier.predict([text_lower])[0]
                proba = self.classifier.predict_proba([text_lower])[0]
                confidence = max(proba)

                return {
                    "service": service,
                    "confidence": float(confidence),
                    "method": "ml_classifier"
                }
            except Exception as e:
                logger.warning(f"Error en clasificador ML: {e}")

        # Fallback: busqueda por palabras clave
        return self._classify_by_keywords(text_lower)

    def _classify_by_keywords(self, text: str) -> Dict[str, Any]:
        """Clasificacion por palabras clave (fallback)"""

        scores = {}

        for service, keywords in self.service_training_data.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    score += 1
            scores[service] = score

        if max(scores.values()) > 0:
            best_service = max(scores, key=scores.get)
            confidence = scores[best_service] / len(self.service_training_data[best_service])
        else:
            best_service = "electrico-residencial"
            confidence = 0.3

        return {
            "service": best_service,
            "confidence": min(1.0, confidence),
            "method": "keyword_matching"
        }

    def extract_entities(self, text: str) -> Dict[str, Any]:
        """
        Extrae entidades del texto usando patrones y NER.

        Args:
            text: Texto a analizar

        Returns:
            Dict con entidades extraidas
        """
        entities = {
            "areas": [],
            "cantidades": [],
            "precios": [],
            "pisos": [],
            "potencias": [],
            "ubicaciones": [],
            "fechas": [],
            "raw_entities": []
        }

        # Extraccion por patrones regex
        for entity_type, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.findall(pattern, text.lower())
                for match in matches:
                    value = match.replace(",", "") if isinstance(match, str) else match
                    try:
                        num_value = float(value)
                        if entity_type == "area":
                            entities["areas"].append(num_value)
                        elif entity_type == "cantidad":
                            entities["cantidades"].append(int(num_value))
                        elif entity_type == "precio":
                            entities["precios"].append(num_value)
                        elif entity_type == "pisos":
                            entities["pisos"].append(int(num_value))
                        elif entity_type == "potencia":
                            entities["potencias"].append(num_value)
                    except ValueError:
                        continue

        # Extraccion con spaCy NER
        if self.nlp:
            try:
                doc = self.nlp(text)

                for ent in doc.ents:
                    entities["raw_entities"].append({
                        "text": ent.text,
                        "label": ent.label_,
                        "start": ent.start_char,
                        "end": ent.end_char
                    })

                    # Clasificar entidades
                    if ent.label_ == "LOC":
                        entities["ubicaciones"].append(ent.text)
                    elif ent.label_ in ["DATE", "TIME"]:
                        entities["fechas"].append(ent.text)

            except Exception as e:
                logger.warning(f"Error en NER spaCy: {e}")

        # Valores principales
        entities["area_principal"] = entities["areas"][0] if entities["areas"] else None
        entities["cantidad_principal"] = entities["cantidades"][0] if entities["cantidades"] else None
        entities["precio_principal"] = entities["precios"][0] if entities["precios"] else None
        entities["num_pisos"] = entities["pisos"][0] if entities["pisos"] else 1

        return entities

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analisis completo del texto.

        Combina clasificacion y extraccion de entidades.

        Args:
            text: Texto a analizar

        Returns:
            Analisis completo
        """
        # Clasificar servicio
        service_result = self.classify_service(text)

        # Extraer entidades
        entities = self.extract_entities(text)

        # Analisis adicional
        analysis = {
            "service": service_result,
            "entities": entities,
            "text_stats": {
                "length": len(text),
                "words": len(text.split()),
                "sentences": len(text.split('.'))
            }
        }

        # Detectar intencion basica
        text_lower = text.lower()
        if any(word in text_lower for word in ["cotizar", "precio", "cuanto", "costo"]):
            analysis["intent"] = "cotizacion"
        elif any(word in text_lower for word in ["proyecto", "planificar", "ejecutar"]):
            analysis["intent"] = "proyecto"
        elif any(word in text_lower for word in ["informe", "reporte", "analisis"]):
            analysis["intent"] = "informe"
        else:
            analysis["intent"] = "consulta"

        return analysis

    def generate_structured_data(
        self,
        text: str,
        document_type: str = "cotizacion"
    ) -> Dict[str, Any]:
        """
        Genera datos estructurados para documentos.

        Args:
            text: Texto del usuario
            document_type: Tipo de documento

        Returns:
            Datos estructurados listos para generar documento
        """
        # Analizar texto
        analysis = self.analyze_text(text)

        # Obtener servicio
        service = analysis["service"]["service"]
        entities = analysis["entities"]

        # Datos base
        data = {
            "servicio": service,
            "area_m2": entities.get("area_principal", 100),
            "num_pisos": entities.get("num_pisos", 1),
            "confianza_clasificacion": analysis["service"]["confidence"]
        }

        # Datos especificos segun tipo
        if document_type == "cotizacion":
            data.update({
                "cliente": "Cliente detectado del texto",
                "items": self._generate_items(service, entities),
                "observaciones": f"Servicio de {service} detectado automaticamente"
            })

        elif document_type == "proyecto":
            data.update({
                "nombre_proyecto": f"Proyecto de {service}",
                "duracion_estimada": self._estimate_duration(service, entities),
                "fases": self._generate_phases(service)
            })

        elif document_type == "informe":
            data.update({
                "titulo": f"Informe de {service}",
                "tipo_informe": "tecnico",
                "secciones": self._generate_sections(service)
            })

        return data

    def _generate_items(
        self,
        service: str,
        entities: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Genera items de cotizacion basados en el servicio"""

        area = entities.get("area_principal", 100)

        # Items base por servicio
        items_templates = {
            "electrico-residencial": [
                {"descripcion": "Tablero electrico", "cantidad": 1, "precio": 450},
                {"descripcion": "Circuitos electricos", "cantidad": max(6, int(area/25)), "precio": 120},
                {"descripcion": "Puntos de luz", "cantidad": int(area/10), "precio": 45},
                {"descripcion": "Tomacorrientes", "cantidad": int(area/15), "precio": 35},
                {"descripcion": "Puesta a tierra", "cantidad": 1, "precio": 850}
            ],
            "contraincendios": [
                {"descripcion": "Central de alarma", "cantidad": 1, "precio": 2500},
                {"descripcion": "Detectores de humo", "cantidad": int(area/20), "precio": 85},
                {"descripcion": "Sirena de alarma", "cantidad": max(2, int(area/100)), "precio": 150},
                {"descripcion": "Pulsadores manuales", "cantidad": max(2, int(area/80)), "precio": 120}
            ]
        }

        items = items_templates.get(service, items_templates["electrico-residencial"])

        # Agregar totales
        for item in items:
            item["unidad"] = "und"
            item["precio_unitario"] = item["precio"]
            item["total"] = item["cantidad"] * item["precio"]
            del item["precio"]

        return items

    def _estimate_duration(
        self,
        service: str,
        entities: Dict[str, Any]
    ) -> str:
        """Estima duracion del proyecto"""

        area = entities.get("area_principal", 100)

        # Dias base por servicio
        base_days = {
            "electrico-residencial": 15,
            "electrico-comercial": 20,
            "electrico-industrial": 30,
            "contraincendios": 25
        }

        days = base_days.get(service, 20)
        days += int(area / 50)  # Adicional por area

        if days <= 7:
            return "1 semana"
        elif days <= 14:
            return "2 semanas"
        elif days <= 21:
            return "3 semanas"
        else:
            weeks = days // 7
            return f"{weeks} semanas"

    def _generate_phases(self, service: str) -> List[Dict[str, Any]]:
        """Genera fases del proyecto"""

        return [
            {"nombre": "Planificacion", "duracion_dias": 5, "entregable": "Plan aprobado"},
            {"nombre": "Ingenieria", "duracion_dias": 7, "entregable": "Planos"},
            {"nombre": "Ejecucion", "duracion_dias": 15, "entregable": "Obra"},
            {"nombre": "Pruebas", "duracion_dias": 3, "entregable": "Certificados"},
            {"nombre": "Cierre", "duracion_dias": 2, "entregable": "Acta"}
        ]

    def _generate_sections(self, service: str) -> List[Dict[str, Any]]:
        """Genera secciones de informe"""

        return [
            {"titulo": "Introduccion", "contenido": f"Informe de {service}"},
            {"titulo": "Marco Normativo", "contenido": "Normativas aplicables"},
            {"titulo": "Descripcion Tecnica", "contenido": "Especificaciones"},
            {"titulo": "Resultados", "contenido": "Conclusiones"}
        ]

    def is_available(self) -> bool:
        """Verifica si el motor esta disponible"""
        return SKLEARN_AVAILABLE or SPACY_AVAILABLE


# Instancia global
ml_engine = MLEngine()

def get_ml_engine() -> MLEngine:
    """Obtiene la instancia del motor ML"""
    return ml_engine
