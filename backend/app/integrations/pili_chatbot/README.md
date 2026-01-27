# PILI ITSE ChatBot - Caja Negra

Módulo autocontenido para chat ITSE.

## 🎯 Concepto: Transformer / Caja Negra

```
INPUT → [PILI_ChatBot] → OUTPUT
```

- **INPUT:** mensaje + estado
- **OUTPUT:** respuesta + nuevo_estado + cotización

## 📦 Uso desde Backend Existente

```python
# En tu backend/app/routers/chat.py
from Pili_ChatBot.pili_itse_chatbot import PILIITSEChatBot

# Crear instancia (una vez)
chatbot = PILIITSEChatBot()

# Usar en endpoint
@router.post("/api/chat/itse")
async def chat_itse(request: ChatRequest):
    resultado = chatbot.procesar(
        mensaje=request.mensaje,
        estado=request.estado
    )
    
    return {
        "success": resultado['success'],
        "respuesta": resultado['respuesta'],
        "botones": resultado['botones'],
        "estado": resultado['estado'],
        "cotizacion": resultado['cotizacion']
    }
```

## ✅ Características

- ✅ **Autocontenido:** No depende de nada externo
- ✅ **Simple:** 1 archivo, ~400 líneas
- ✅ **Funcional:** Basado en código que FUNCIONA
- ✅ **Testeable:** Incluye test en `if __name__ == "__main__"`

## 🧪 Testing

```bash
cd Pili_ChatBot
python pili_itse_chatbot.py
```

## 📋 Estructura

```
Pili_ChatBot/
├── pili_itse_chatbot.py  # Módulo principal
├── README.md              # Este archivo
└── __init__.py            # Para importar como paquete
```

## 🔌 Integración

NO necesitas modificar:
- ❌ Backend existente
- ❌ Frontend existente
- ❌ Base de datos

SOLO necesitas:
- ✅ Importar el módulo
- ✅ Llamar a `chatbot.procesar()`
- ✅ Retornar el resultado
