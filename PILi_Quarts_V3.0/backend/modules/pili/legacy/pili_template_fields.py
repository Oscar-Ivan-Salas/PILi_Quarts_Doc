"""
MAPEO DE CAMPOS REQUERIDOS POR TIPO DE DOCUMENTO
Este archivo define exactamente qué campos necesita PILI para cada plantilla editable
"""

# Campos requeridos para cada tipo de documento
CAMPOS_POR_DOCUMENTO = {
    "cotizacion-simple": {
        "cliente": {
            "nombre": {"tipo": "texto", "pregunta": "👤 ¿Cuál es el nombre del cliente?", "requerido": True},
            "ruc": {"tipo": "texto", "pregunta": "📋 ¿RUC del cliente? (opcional)", "requerido": False},
            "direccion": {"tipo": "texto", "pregunta": "📍 ¿Dirección del cliente? (opcional)", "requerido": False},
            "telefono": {"tipo": "texto", "pregunta": "📞 ¿Teléfono del cliente? (opcional)", "requerido": False},
            "email": {"tipo": "texto", "pregunta": "📧 ¿Email del cliente? (opcional)", "requerido": False}
        },
        "proyecto": {
            "nombre": {"tipo": "texto", "pregunta": "🏗️ ¿Nombre del proyecto?", "requerido": True},
            "area_m2": {"tipo": "numero", "pregunta": "📏 ¿Área del proyecto en m²?", "requerido": True}
        },
        "servicio": {
            "tipo": {"tipo": "seleccion", "pregunta": "⚡ ¿Qué tipo de servicio eléctrico?", "opciones": [
                "Instalaciones Eléctricas Residenciales",
                "Instalaciones Eléctricas Comerciales",
                "Instalaciones Eléctricas Industriales",
                "Sistemas de Puesta a Tierra",
                "Sistemas Contraincendios"
            ], "requerido": True}
        },
        "detalles_tecnicos": {
            "cantidad_puntos": {"tipo": "numero", "pregunta": "💡 ¿Cuántos puntos de luz?", "requerido": True},
            "cantidad_tomacorrientes": {"tipo": "numero", "pregunta": "🔌 ¿Cuántos tomacorrientes?", "requerido": True},
            "num_pisos": {"tipo": "numero", "pregunta": "🏢 ¿Cuántos pisos?", "requerido": False, "default": 1}
        }
    },
    
    "cotizacion-compleja": {
        "cliente": {
            "nombre": {"tipo": "texto", "pregunta": "👤 ¿Nombre del cliente?", "requerido": True},
            "ruc": {"tipo": "texto", "pregunta": "📋 ¿RUC?", "requerido": True},
            "direccion": {"tipo": "texto", "pregunta": "📍 ¿Dirección?", "requerido": True}
        },
        "proyecto": {
            "nombre": {"tipo": "texto", "pregunta": "🏗️ ¿Nombre del proyecto?", "requerido": True},
            "area_m2": {"tipo": "numero", "pregunta": "📏 ¿Área en m²?", "requerido": True},
            "potencia_kw": {"tipo": "numero", "pregunta": "⚡ ¿Potencia requerida en kW?", "requerido": True}
        },
        "servicio": {
            "tipo": {"tipo": "seleccion", "pregunta": "⚡ ¿Tipo de servicio?", "opciones": [
                "Instalaciones Eléctricas Comerciales",
                "Instalaciones Eléctricas Industriales",
                "Sistemas Contraincendios",
                "Domótica y Automatización"
            ], "requerido": True}
        },
        "detalles_tecnicos": {
            "cantidad_puntos": {"tipo": "numero", "pregunta": "💡 ¿Puntos de luz?", "requerido": True},
            "cantidad_tomacorrientes": {"tipo": "numero", "pregunta": "🔌 ¿Tomacorrientes?", "requerido": True},
            "num_pisos": {"tipo": "numero", "pregunta": "🏢 ¿Pisos?", "requerido": True},
            "cantidad_interruptores": {"tipo": "numero", "pregunta": "🔘 ¿Interruptores?", "requerido": False}
        }
    },
    
    "proyecto-simple": {
        "cliente": {
            "nombre": {"tipo": "texto", "pregunta": "👤 ¿Cliente?", "requerido": True}
        },
        "proyecto": {
            "nombre": {"tipo": "texto", "pregunta": "🏗️ ¿Nombre del proyecto?", "requerido": True},
            "duracion": {"tipo": "texto", "pregunta": "📅 ¿Duración estimada? (ej: 3 meses)", "requerido": True},
            "presupuesto": {"tipo": "numero", "pregunta": "💰 ¿Presupuesto estimado?", "requerido": False}
        },
        "alcance": {
            "descripcion": {"tipo": "texto_largo", "pregunta": "📝 ¿Descripción del alcance del proyecto?", "requerido": True}
        }
    },
    
    "proyecto-complejo": {
        "cliente": {
            "nombre": {"tipo": "texto", "pregunta": "👤 ¿Cliente?", "requerido": True},
            "ruc": {"tipo": "texto", "pregunta": "📋 ¿RUC?", "requerido": True}
        },
        "proyecto": {
            "nombre": {"tipo": "texto", "pregunta": "🏗️ ¿Nombre del proyecto?", "requerido": True},
            "duracion": {"tipo": "texto", "pregunta": "📅 ¿Duración?", "requerido": True},
            "presupuesto": {"tipo": "numero", "pregunta": "💰 ¿Presupuesto?", "requerido": True},
            "area_m2": {"tipo": "numero", "pregunta": "📏 ¿Área en m²?", "requerido": True}
        },
        "alcance": {
            "descripcion": {"tipo": "texto_largo", "pregunta": "📝 ¿Alcance del proyecto?", "requerido": True},
            "entregables": {"tipo": "lista", "pregunta": "📦 ¿Principales entregables?", "requerido": True}
        }
    },
    
    "informe-simple": {
        "cliente": {
            "nombre": {"tipo": "texto", "pregunta": "👤 ¿Cliente?", "requerido": True}
        },
        "informe": {
            "titulo": {"tipo": "texto", "pregunta": "📄 ¿Título del informe?", "requerido": True},
            "tipo_instalacion": {"tipo": "seleccion", "pregunta": "⚡ ¿Tipo de instalación?", "opciones": [
                "Instalación Eléctrica Residencial",
                "Instalación Eléctrica Comercial",
                "Sistema de Puesta a Tierra",
                "Sistema Contraincendios"
            ], "requerido": True}
        },
        "detalles": {
            "area_m2": {"tipo": "numero", "pregunta": "📏 ¿Área evaluada en m²?", "requerido": True},
            "ubicacion": {"tipo": "texto", "pregunta": "📍 ¿Ubicación?", "requerido": True}
        }
    },
    
    "informe-ejecutivo": {
        "cliente": {
            "nombre": {"tipo": "texto", "pregunta": "👤 ¿Cliente?", "requerido": True},
            "ruc": {"tipo": "texto", "pregunta": "📋 ¿RUC?", "requerido": True}
        },
        "informe": {
            "titulo": {"tipo": "texto", "pregunta": "📄 ¿Título del informe?", "requerido": True},
            "tipo_instalacion": {"tipo": "seleccion", "pregunta": "⚡ ¿Tipo de instalación?", "opciones": [
                "Instalación Eléctrica Industrial",
                "Sistema Contraincendios Completo",
                "Expediente Técnico",
                "ITSE"
            ], "requerido": True}
        },
        "detalles": {
            "area_m2": {"tipo": "numero", "pregunta": "📏 ¿Área en m²?", "requerido": True},
            "ubicacion": {"tipo": "texto", "pregunta": "📍 ¿Ubicación?", "requerido": True},
            "potencia_kw": {"tipo": "numero", "pregunta": "⚡ ¿Potencia en kW?", "requerido": True}
        }
    }
}


def obtener_campos_requeridos(tipo_documento):
    """
    Retorna lista plana de campos requeridos para un tipo de documento
    """
    campos = CAMPOS_POR_DOCUMENTO.get(tipo_documento, {})
    campos_planos = []
    
    for seccion, campos_seccion in campos.items():
        for campo, config in campos_seccion.items():
            if config.get("requerido", False):
                campos_planos.append({
                    "seccion": seccion,
                    "campo": campo,
                    "tipo": config["tipo"],
                    "pregunta": config["pregunta"],
                    "opciones": config.get("opciones", [])
                })
    
    return campos_planos


def obtener_siguiente_pregunta(tipo_documento, datos_actuales):
    """
    Determina cuál es la siguiente pregunta que PILI debe hacer
    basándose en los datos que ya tiene
    """
    campos_requeridos = obtener_campos_requeridos(tipo_documento)
    
    for campo_info in campos_requeridos:
        seccion = campo_info["seccion"]
        campo = campo_info["campo"]
        
        # Verificar si ya tenemos este dato
        if seccion in datos_actuales and campo in datos_actuales[seccion]:
            continue  # Ya tenemos este dato
        
        # Este es el siguiente dato que falta
        return campo_info
    
    # Si llegamos aquí, tenemos todos los datos
    return None


# Ejemplo de uso:
if __name__ == "__main__":
    # Ejemplo para cotización simple
    print("=== COTIZACIÓN SIMPLE ===")
    campos = obtener_campos_requeridos("cotizacion-simple")
    for campo in campos:
        print(f"{campo['pregunta']}")
    
    print("\n=== INFORME SIMPLE ===")
    campos = obtener_campos_requeridos("informe-simple")
    for campo in campos:
        print(f"{campo['pregunta']}")
