#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Simulación RALFTH - Generación Masiva de Documentos
Simula 3 usuarios reales generando 6 tipos de documentos en 3 formatos
Total: 3 usuarios × 6 tipos × 3 formatos = 54 documentos
"""

import requests
import json
from datetime import datetime
from pathlib import Path

# Configuración
API_BASE = "http://localhost:8005/api/generate"
OUTPUT_DIR = Path("e:/PILi_Quarts/PILi_Quarts_V3.0/backend/generated")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# USUARIO 1: ACEROS DEL PERÚ S.A.C.
# ============================================================================
usuario1 = {
    "emisor": {
        "nombre": "ACEROS DEL PERÚ S.A.C.",
        "empresa": "ACEROS DEL PERÚ S.A.C.",
        "ruc": "20456789012",
        "direccion": "Av. Industrial 456, Callao",
        "telefono": "01-4567890",
        "email": "ventas@acerosdelperu.com"
    },
    "cliente": {
        "nombre": "MINERA DEL SUR S.A.",
        "ruc": "20123456789"
    },
    "proyecto": {
        "nombre": "Estructuras Metálicas Planta Lima"
    }
}

# Cotización Simple - Usuario 1
cotizacion_simple_u1 = {
    **usuario1,
    "numero": "COT-001-2026",
    "fecha": datetime.now().strftime('%d/%m/%Y'),
    "vigencia": "30 días",
    "servicio": "Fabricación de Estructuras Metálicas",
    "area_m2": "500",
    "items": [
        {
            "descripcion": "Vigas de Acero H 200x200",
            "cantidad": 50,
            "unidad": "und",
            "precio_unitario": 850.00,
            "precioUnitario": 850.00
        },
        {
            "descripcion": "Columnas Metálicas 300x300",
            "cantidad": 30,
            "unidad": "und",
            "precio_unitario": 1200.00,
            "precioUnitario": 1200.00
        },
        {
            "descripcion": "Planchas de Acero A36 6mm",
            "cantidad": 100,
            "unidad": "m²",
            "precio_unitario": 180.00,
            "precioUnitario": 180.00
        }
    ],
    "suministros": [
        {
            "descripcion": "Vigas de Acero H 200x200",
            "cantidad": 50,
            "precioUnitario": 850.00,
            "precioTotal": 42500.00
        },
        {
            "descripcion": "Columnas Metálicas 300x300",
            "cantidad": 30,
            "precioUnitario": 1200.00,
            "precioTotal": 36000.00
        },
        {
            "descripcion": "Planchas de Acero A36 6mm",
            "cantidad": 100,
            "precioUnitario": 180.00,
            "precioTotal": 18000.00
        }
    ]
}

# Cotización Compleja - Usuario 1
cotizacion_compleja_u1 = {
    **usuario1,
    "numero": "COT-002-2026",
    "fecha": datetime.now().strftime('%d/%m/%Y'),
    "items": cotizacion_simple_u1["items"]
}

# Proyecto Simple - Usuario 1
proyecto_simple_u1 = {
    **usuario1,
    "fases": [
        {
            "nombre": "Diseño Estructural",
            "duracion": 15,
            "costo": 8500.00
        },
        {
            "nombre": "Fabricación",
            "duracion": 45,
            "costo": 85000.00
        },
        {
            "nombre": "Montaje",
            "duracion": 20,
            "costo": 25000.00
        }
    ]
}

# Proyecto Complejo PMI - Usuario 1
proyecto_complejo_u1 = {
    **usuario1,
    "fases": proyecto_simple_u1["fases"],
    "riesgos": [
        {
            "descripcion": "Retraso en entrega de materiales",
            "probabilidad": "Media",
            "impacto": "Alto",
            "mitigacion": "Contratos con proveedores alternativos"
        },
        {
            "descripcion": "Condiciones climáticas adversas",
            "probabilidad": "Baja",
            "impacto": "Medio",
            "mitigacion": "Plan de contingencia para trabajo bajo techo"
        }
    ]
}

# Informe Técnico - Usuario 1
informe_tecnico_u1 = {
    **usuario1,
    "informe": {
        "titulo": "Inspección Técnica Estructuras Metálicas",
        "fecha": datetime.now().strftime('%d/%m/%Y'),
        "inspector": "Ing. Carlos Mendoza"
    },
    "hallazgos": [
        {
            "descripcion": "Corrosión en vigas principales",
            "severidad": "Media",
            "recomendacion": "Aplicar tratamiento anticorrosivo"
        },
        {
            "descripcion": "Soldaduras con fisuras menores",
            "severidad": "Baja",
            "recomendacion": "Reforzar soldaduras afectadas"
        }
    ]
}

# Informe Ejecutivo APA - Usuario 1
informe_ejecutivo_u1 = {
    **usuario1,
    "informe": informe_tecnico_u1["informe"],
    "conclusiones": [
        "Las estructuras metálicas requieren mantenimiento preventivo",
        "Se recomienda inspección trimestral",
        "Vida útil estimada: 15 años con mantenimiento adecuado"
    ]
}

# ============================================================================
# USUARIO 2: PILi Ingeniería E.I.R.L.
# ============================================================================
usuario2 = {
    "emisor": {
        "nombre": "PILi Ingeniería E.I.R.L.",
        "empresa": "PILi Ingeniería E.I.R.L.",
        "ruc": "20987654321",
        "direccion": "Jr. Los Electricistas 789, San Juan de Lurigancho",
        "telefono": "01-9876543",
        "email": "contacto@piliingenieria.pe"
    },
    "cliente": {
        "nombre": "CONSTRUCTORA LIMA S.A.C.",
        "ruc": "20555666777"
    },
    "proyecto": {
        "nombre": "Sistema Eléctrico Edificio Comercial"
    }
}

# Cotización Simple - Usuario 2
cotizacion_simple_u2 = {
    **usuario2,
    "numero": "COT-003-2026",
    "fecha": datetime.now().strftime('%d/%m/%Y'),
    "vigencia": "45 días",
    "servicio": "Instalaciones Eléctricas Comerciales",
    "area_m2": "800",
    "items": [
        {
            "descripcion": "Puesta a Tierra Completa",
            "cantidad": 1,
            "unidad": "glb",
            "precio_unitario": 3500.00,
            "precioUnitario": 3500.00
        },
        {
            "descripcion": "Tablero Eléctrico Trifásico 400A",
            "cantidad": 2,
            "unidad": "und",
            "precio_unitario": 2800.00,
            "precioUnitario": 2800.00
        },
        {
            "descripcion": "Cableado Estructurado Cat6",
            "cantidad": 500,
            "unidad": "m",
            "precio_unitario": 15.50,
            "precioUnitario": 15.50
        }
    ],
    "suministros": [
        {
            "descripcion": "Puesta a Tierra Completa",
            "cantidad": 1,
            "precioUnitario": 3500.00,
            "precioTotal": 3500.00
        },
        {
            "descripcion": "Tablero Eléctrico Trifásico 400A",
            "cantidad": 2,
            "precioUnitario": 2800.00,
            "precioTotal": 5600.00
        },
        {
            "descripcion": "Cableado Estructurado Cat6",
            "cantidad": 500,
            "precioUnitario": 15.50,
            "precioTotal": 7750.00
        }
    ]
}

# Cotización Compleja - Usuario 2
cotizacion_compleja_u2 = {
    **usuario2,
    "numero": "COT-004-2026",
    "fecha": datetime.now().strftime('%d/%m/%Y'),
    "items": cotizacion_simple_u2["items"]
}

# Proyecto Simple - Usuario 2
proyecto_simple_u2 = {
    **usuario2,
    "fases": [
        {
            "nombre": "Diseño Eléctrico",
            "duracion": 10,
            "costo": 5500.00
        },
        {
            "nombre": "Instalación",
            "duracion": 30,
            "costo": 18000.00
        },
        {
            "nombre": "Pruebas y Certificación",
            "duracion": 5,
            "costo": 3500.00
        }
    ]
}

# Proyecto Complejo PMI - Usuario 2
proyecto_complejo_u2 = {
    **usuario2,
    "fases": proyecto_simple_u2["fases"],
    "riesgos": [
        {
            "descripcion": "Interferencia con sistemas existentes",
            "probabilidad": "Alta",
            "impacto": "Alto",
            "mitigacion": "Levantamiento detallado previo"
        }
    ]
}

# Informe Técnico - Usuario 2
informe_tecnico_u2 = {
    **usuario2,
    "informe": {
        "titulo": "Auditoría Eléctrica Edificio Comercial",
        "fecha": datetime.now().strftime('%d/%m/%Y'),
        "inspector": "Ing. María Torres"
    },
    "hallazgos": [
        {
            "descripcion": "Sobrecarga en circuito de iluminación",
            "severidad": "Alta",
            "recomendacion": "Redistribuir cargas y agregar circuito adicional"
        }
    ]
}

# Informe Ejecutivo APA - Usuario 2
informe_ejecutivo_u2 = {
    **usuario2,
    "informe": informe_tecnico_u2["informe"],
    "conclusiones": [
        "Sistema eléctrico requiere actualización urgente",
        "Riesgo de sobrecarga en horas pico"
    ]
}

# ============================================================================
# USUARIO 3: SERVICIOS INDUSTRIALES DEL NORTE S.R.L.
# ============================================================================
usuario3 = {
    "emisor": {
        "nombre": "SERVICIOS INDUSTRIALES DEL NORTE S.R.L.",
        "empresa": "SERVICIOS INDUSTRIALES DEL NORTE S.R.L.",
        "ruc": "20111222333",
        "direccion": "Av. Panamericana Norte Km 15, Ancón",
        "telefono": "01-2223344",
        "email": "ventas@sidnorte.com.pe"
    },
    "cliente": {
        "nombre": "PESQUERA PACIFICO S.A.",
        "ruc": "20888999000"
    },
    "proyecto": {
        "nombre": "Mantenimiento Eléctrico Planta Procesadora"
    }
}

# Cotización Simple - Usuario 3
cotizacion_simple_u3 = {
    **usuario3,
    "numero": "COT-005-2026",
    "fecha": datetime.now().strftime('%d/%m/%Y'),
    "vigencia": "60 días",
    "servicio": "Mantenimiento Industrial",
    "area_m2": "1200",
    "items": [
        {
            "descripcion": "Mantenimiento Preventivo Subestación",
            "cantidad": 1,
            "unidad": "glb",
            "precio_unitario": 8500.00,
            "precioUnitario": 8500.00
        },
        {
            "descripcion": "Reemplazo de Transformador 500KVA",
            "cantidad": 1,
            "unidad": "und",
            "precio_unitario": 45000.00,
            "precioUnitario": 45000.00
        }
    ],
    "suministros": [
        {
            "descripcion": "Mantenimiento Preventivo Subestación",
            "cantidad": 1,
            "precioUnitario": 8500.00,
            "precioTotal": 8500.00
        },
        {
            "descripcion": "Reemplazo de Transformador 500KVA",
            "cantidad": 1,
            "precioUnitario": 45000.00,
            "precioTotal": 45000.00
        }
    ]
}

# Cotización Compleja - Usuario 3
cotizacion_compleja_u3 = {
    **usuario3,
    "numero": "COT-006-2026",
    "fecha": datetime.now().strftime('%d/%m/%Y'),
    "items": cotizacion_simple_u3["items"]
}

# Proyecto Simple - Usuario 3
proyecto_simple_u3 = {
    **usuario3,
    "fases": [
        {
            "nombre": "Diagnóstico",
            "duracion": 5,
            "costo": 4500.00
        },
        {
            "nombre": "Mantenimiento",
            "duracion": 15,
            "costo": 35000.00
        },
        {
            "nombre": "Pruebas Finales",
            "duracion": 3,
            "costo": 2500.00
        }
    ]
}

# Proyecto Complejo PMI - Usuario 3
proyecto_complejo_u3 = {
    **usuario3,
    "fases": proyecto_simple_u3["fases"],
    "riesgos": [
        {
            "descripcion": "Parada de planta no programada",
            "probabilidad": "Media",
            "impacto": "Crítico",
            "mitigacion": "Trabajo en horarios de baja producción"
        }
    ]
}

# Informe Técnico - Usuario 3
informe_tecnico_u3 = {
    **usuario3,
    "informe": {
        "titulo": "Inspección Subestación Eléctrica",
        "fecha": datetime.now().strftime('%d/%m/%Y'),
        "inspector": "Ing. Roberto Sánchez"
    },
    "hallazgos": [
        {
            "descripcion": "Transformador con temperatura elevada",
            "severidad": "Crítica",
            "recomendacion": "Reemplazo inmediato"
        }
    ]
}

# Informe Ejecutivo APA - Usuario 3
informe_ejecutivo_u3 = {
    **usuario3,
    "informe": informe_tecnico_u3["informe"],
    "conclusiones": [
        "Transformador en estado crítico",
        "Reemplazo urgente requerido para evitar parada de planta"
    ]
}

# ============================================================================
# FUNCIÓN DE GENERACIÓN
# ============================================================================
def generar_documento(usuario_nombre, doc_tipo, formato, datos):
    """Genera un documento llamando al backend"""
    
    endpoints = {
        "word": f"{API_BASE}/word",
        "excel": f"{API_BASE}/excel",
        "pdf": f"{API_BASE}/pdf"
    }
    
    endpoint = endpoints.get(formato)
    if not endpoint:
        print(f"❌ Formato desconocido: {formato}")
        return False
    
    payload = {
        "title": f"{usuario_nombre}_{doc_tipo}",
        "data": datos,
        "user_id": usuario_nombre.lower().replace(" ", "_"),
        "doc_type": doc_tipo,
        "personalizacion": {
            "esquemaColores": "azul-tesla",
            "logoBase64": None,
            "ocultarIGV": False
        }
    }
    
    try:
        print(f"📤 Generando: {usuario_nombre} - {doc_tipo} - {formato.upper()}")
        response = requests.post(endpoint, json=payload, timeout=60)
        
        if response.status_code == 200:
            # Guardar archivo
            extension = {"word": "docx", "excel": "xlsx", "pdf": "pdf"}[formato]
            filename = f"{usuario_nombre}_{doc_tipo}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"
            filepath = OUTPUT_DIR / filename
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Guardado: {filepath}")
            return True
        else:
            print(f"❌ Error {response.status_code}: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Excepción: {str(e)}")
        return False

# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================
if __name__ == "__main__":
    print("=" * 80)
    print("🎭 SIMULACIÓN RALFTH - Generación Masiva de Documentos")
    print("=" * 80)
    print(f"📁 Directorio de salida: {OUTPUT_DIR}")
    print(f"🌐 API Backend: {API_BASE}")
    print("=" * 80)
    
    usuarios = [
        ("ACEROS_DEL_PERU", {
            "Cotizacion_Simple": cotizacion_simple_u1,
            "Cotizacion_Compleja": cotizacion_compleja_u1,
            "Proyecto_Simple": proyecto_simple_u1,
            "Proyecto_Complejo_PMI": proyecto_complejo_u1,
            "Informe_Tecnico": informe_tecnico_u1,
            "Informe_Ejecutivo_APA": informe_ejecutivo_u1
        }),
        ("PILI_INGENIERIA", {
            "Cotizacion_Simple": cotizacion_simple_u2,
            "Cotizacion_Compleja": cotizacion_compleja_u2,
            "Proyecto_Simple": proyecto_simple_u2,
            "Proyecto_Complejo_PMI": proyecto_complejo_u2,
            "Informe_Tecnico": informe_tecnico_u2,
            "Informe_Ejecutivo_APA": informe_ejecutivo_u2
        }),
        ("SERVICIOS_INDUSTRIALES_NORTE", {
            "Cotizacion_Simple": cotizacion_simple_u3,
            "Cotizacion_Compleja": cotizacion_compleja_u3,
            "Proyecto_Simple": proyecto_simple_u3,
            "Proyecto_Complejo_PMI": proyecto_complejo_u3,
            "Informe_Tecnico": informe_tecnico_u3,
            "Informe_Ejecutivo_APA": informe_ejecutivo_u3
        })
    ]
    
    formatos = ["word", "excel", "pdf"]
    
    total = 0
    exitosos = 0
    fallidos = 0
    
    for usuario_nombre, documentos in usuarios:
        print(f"\n{'=' * 80}")
        print(f"👤 USUARIO: {usuario_nombre}")
        print(f"{'=' * 80}")
        
        for doc_tipo, datos in documentos.items():
            for formato in formatos:
                total += 1
                if generar_documento(usuario_nombre, doc_tipo, formato, datos):
                    exitosos += 1
                else:
                    fallidos += 1
    
    print("\n" + "=" * 80)
    print("📊 RESUMEN FINAL")
    print("=" * 80)
    print(f"Total documentos: {total}")
    print(f"✅ Exitosos: {exitosos}")
    print(f"❌ Fallidos: {fallidos}")
    print(f"📁 Ubicación: {OUTPUT_DIR}")
    print("=" * 80)
