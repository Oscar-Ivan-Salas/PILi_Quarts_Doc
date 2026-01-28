# 🎯 Plan Detallado de Migración de BD - 20 Pasos

**Fecha:** 2026-01-08  
**Objetivo:** Migrar BD sin romper funcionalidad existente  
**Tiempo Total:** 3 horas  
**Checkpoints:** 5 puntos de aprobación

---

## 📊 Estado Actual de la BD

### **Tablas Existentes (6):**

```
1. usuarios          ❌ NO EXISTE (crear)
2. clientes          ✅ EXISTE (NO tocar)
3. proyectos         ✅ EXISTE (AGREGAR campos)
4. cotizaciones      ✅ EXISTE (NO tocar)
5. items             ✅ EXISTE (NO tocar)
6. documentos        ✅ EXISTE (NO tocar)
```

### **Documentos Funcionando (3 de 6):**

```
✅ 1. Cotización Simple
✅ 2. Cotización Compleja
✅ 3. Proyecto Complejo PMI
⏳ 4. Proyecto Simple (parcial)
❌ 5. Informe Técnico
❌ 6. Informe Ejecutivo APA
```

### **Campos a Agregar en `proyectos`:**

```python
servicio = Column(String(50), nullable=True)
industria = Column(String(50), nullable=True)
presupuesto = Column(Numeric(12, 2), nullable=True)
moneda = Column(String(3), default='PEN', nullable=True)
duracion_total = Column(Integer, nullable=True)
tipo_dias = Column(String(20), default='habiles', nullable=True)
area_m2 = Column(Numeric(10, 2), nullable=True)
tiene_area = Column(Boolean, default=False, nullable=True)
alcance_proyecto = Column(Text, nullable=True)
ubicacion = Column(String(200), nullable=True)
normativa = Column(String(200), nullable=True)
```

---

## 🔄 Plan de 20 Pasos

### **FASE 1: PREPARACIÓN Y BACKUP** (30 min)

#### ✅ Paso 1: Verificar BD Actual
**Objetivo:** Confirmar que BD existe y tiene datos  
**Comando:**
```bash
cd backend
python -c "from app.core.database import engine; print(engine.table_names())"
```
**Criterio de Éxito:** Lista de 5 tablas (clientes, proyectos, cotizaciones, items, documentos)  
**Checkpoint:** ⏸️ Informar al usuario

---

#### ✅ Paso 2: Backup de BD
**Objetivo:** Copiar BD actual por seguridad  
**Comando:**
```bash
copy backend\database.db backend\database_backup_2026-01-08.db
```
**Criterio de Éxito:** Archivo `database_backup_2026-01-08.db` creado  
**Checkpoint:** ⏸️ Confirmar backup exitoso

---

#### ✅ Paso 3: Instalar Alembic
**Objetivo:** Herramienta para migraciones  
**Comando:**
```bash
cd backend
pip install alembic
```
**Criterio de Éxito:** Alembic instalado sin errores

---

#### ✅ Paso 4: Inicializar Alembic
**Objetivo:** Configurar sistema de migraciones  
**Comando:**
```bash
cd backend
alembic init alembic
```
**Criterio de Éxito:** Carpeta `alembic/` creada

---

#### ✅ Paso 5: Configurar Alembic
**Objetivo:** Conectar Alembic con nuestra BD  
**Archivo:** `backend/alembic/env.py`  
**Cambios:**
```python
# Línea 18
from app.core.database import Base
from app.models import cliente, cotizacion, documento, item, proyecto

# Línea 21
target_metadata = Base.metadata
```
**Criterio de Éxito:** Alembic puede detectar modelos

---

### **CHECKPOINT 1** ⏸️
**Pregunta al usuario:** "Backup creado y Alembic configurado. ¿Continuar con modificación de modelos?"

---

### **FASE 2: MODIFICAR MODELOS** (30 min)

#### ✅ Paso 6: Crear Modelo Usuario
**Objetivo:** Nuevo modelo para datos del usuario  
**Archivo:** `backend/app/models/usuario.py` (NUEVO)  
**Código:**
```python
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=True, index=True)
    empresa = Column(String(200), nullable=True)
    telefono = Column(String(20), nullable=True)
    logo_base64 = Column(Text, nullable=True)
    
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_modificacion = Column(DateTime(timezone=True), onupdate=func.now())
```
**Criterio de Éxito:** Archivo creado sin errores de sintaxis

---

#### ✅ Paso 7: Actualizar __init__.py
**Objetivo:** Registrar nuevo modelo  
**Archivo:** `backend/app/models/__init__.py`  
**Cambio:** Agregar línea
```python
from .usuario import Usuario
```
**Criterio de Éxito:** Import sin errores

---

#### ✅ Paso 8: Agregar Campos a Proyecto
**Objetivo:** Agregar 11 campos nuevos  
**Archivo:** `backend/app/models/proyecto.py`  
**Ubicación:** Después de línea 33 (después de `estado`)  
**Código a agregar:**
```python
    # ✅ NUEVOS CAMPOS PARA PMI
    servicio = Column(String(50), nullable=True, index=True)
    industria = Column(String(50), nullable=True, index=True)
    presupuesto = Column(Numeric(12, 2), nullable=True)
    moneda = Column(String(3), default='PEN', nullable=True)
    duracion_total = Column(Integer, nullable=True)
    tipo_dias = Column(String(20), default='habiles', nullable=True)
    area_m2 = Column(Numeric(10, 2), nullable=True)
    tiene_area = Column(Boolean, default=False, nullable=True)
    alcance_proyecto = Column(Text, nullable=True)
    ubicacion = Column(String(200), nullable=True)
    normativa = Column(String(200), nullable=True)
```
**Criterio de Éxito:** Modelo sin errores de sintaxis

---

#### ✅ Paso 9: Actualizar to_dict() de Proyecto
**Objetivo:** Incluir nuevos campos en serialización  
**Archivo:** `backend/app/models/proyecto.py`  
**Ubicación:** Dentro de método `to_dict()` (línea 63)  
**Código a agregar:**
```python
            "servicio": self.servicio,
            "industria": self.industria,
            "presupuesto": float(self.presupuesto) if self.presupuesto else None,
            "moneda": self.moneda,
            "duracion_total": self.duracion_total,
            "tipo_dias": self.tipo_dias,
            "area_m2": float(self.area_m2) if self.area_m2 else None,
            "tiene_area": self.tiene_area,
            "alcance_proyecto": self.alcance_proyecto,
            "ubicacion": self.ubicacion,
            "normativa": self.normativa,
```
**Criterio de Éxito:** Método retorna diccionario completo

---

#### ✅ Paso 10: Commit de Cambios
**Objetivo:** Guardar cambios en Git  
**Comando:**
```bash
git add backend/app/models/
git commit -m "feat: Agregar modelo Usuario y campos a Proyecto (nullable)"
```
**Criterio de Éxito:** Commit exitoso

---

### **CHECKPOINT 2** ⏸️
**Pregunta al usuario:** "Modelos actualizados. ¿Continuar con migración de BD?"

---

### **FASE 3: MIGRACIÓN DE BD** (45 min)

#### ✅ Paso 11: Generar Migración
**Objetivo:** Crear script de migración automático  
**Comando:**
```bash
cd backend
alembic revision --autogenerate -m "Agregar tabla usuarios y campos a proyectos"
```
**Criterio de Éxito:** Archivo de migración creado en `alembic/versions/`

---

#### ✅ Paso 12: Revisar Script de Migración
**Objetivo:** Verificar que migración es correcta  
**Archivo:** `backend/alembic/versions/XXXXX_agregar_tabla_usuarios.py`  
**Verificar:**
- ✅ Crea tabla `usuarios`
- ✅ Agrega 11 columnas a `proyectos`
- ✅ NO toca `cotizaciones`, `items`, `documentos`
**Criterio de Éxito:** Script correcto

---

#### ✅ Paso 13: Aplicar Migración
**Objetivo:** Ejecutar migración en BD  
**Comando:**
```bash
cd backend
alembic upgrade head
```
**Criterio de Éxito:** Migración exitosa sin errores

---

#### ✅ Paso 14: Verificar BD Migrada
**Objetivo:** Confirmar que cambios se aplicaron  
**Comando:**
```bash
python -c "from app.models.proyecto import Proyecto; print(Proyecto.__table__.columns.keys())"
```
**Criterio de Éxito:** Lista incluye nuevos campos (servicio, industria, etc.)

---

### **CHECKPOINT 3** ⏸️
**Pregunta al usuario:** "BD migrada exitosamente. ¿Continuar con endpoints?"

---

### **FASE 4: CREAR ENDPOINTS** (45 min)

#### ✅ Paso 15: Crear Router de Proyectos
**Objetivo:** Endpoints para guardar/leer proyectos  
**Archivo:** `backend/app/routers/proyectos.py` (NUEVO)  
**Código:** (Ver implementation_plan.md Fase 2.1)  
**Criterio de Éxito:** Endpoints `POST /proyectos` y `GET /proyectos/{id}` funcionan

---

#### ✅ Paso 16: Registrar Router
**Objetivo:** Activar endpoints en API  
**Archivo:** `backend/app/main.py`  
**Cambio:** Agregar
```python
from app.routers import proyectos
app.include_router(proyectos.router, prefix="/api", tags=["proyectos"])
```
**Criterio de Éxito:** Endpoints visibles en `/docs`

---

#### ✅ Paso 17: Crear Router de Usuarios
**Objetivo:** Endpoints para auto-relleno de usuario  
**Archivo:** `backend/app/routers/usuarios.py` (NUEVO)  
**Endpoints:**
- `POST /usuarios` - Crear usuario
- `GET /usuarios/{id}` - Obtener usuario
**Criterio de Éxito:** Endpoints funcionan

---

#### ✅ Paso 18: Crear Endpoint Auto-relleno Cliente
**Objetivo:** Buscar cliente por RUC  
**Archivo:** `backend/app/routers/clientes.py`  
**Endpoint:** `GET /clientes/buscar?ruc={ruc}`  
**Criterio de Éxito:** Retorna datos del cliente si existe

---

### **CHECKPOINT 4** ⏸️
**Pregunta al usuario:** "Endpoints creados. ¿Probar con Postman o continuar con frontend?"

---

### **FASE 5: CONECTAR FRONTEND** (30 min)

#### ✅ Paso 19: Actualizar App.jsx - Guardar Proyecto
**Objetivo:** Formulario guarda en BD al iniciar chat  
**Archivo:** `frontend/src/App.jsx`  
**Función:** `guardarProyectoEnBD()` (Ver implementation_plan.md Fase 2.2)  
**Criterio de Éxito:** Proyecto se guarda en BD y retorna ID

---

#### ✅ Paso 20: Actualizar Chat - Leer desde BD
**Objetivo:** Chat recibe proyecto_id y carga datos  
**Archivo:** `frontend/src/components/PiliElectricidadProyectoComplejoPMIChat.jsx`  
**Cambio:** Pasar `proyectoId` en estadoInicial  
**Criterio de Éxito:** Chat no pregunta datos ya guardados

---

### **CHECKPOINT 5 FINAL** ⏸️
**Pregunta al usuario:** "Sistema completo. ¿Probar flujo completo?"

---

## ✅ Prueba Final

### **Flujo a Probar:**

1. Llenar formulario inicial
2. Click "Conversar con PILI"
3. Verificar que proyecto se guarda en BD
4. Verificar que chat NO pregunta datos del formulario
5. Completar chat
6. Generar documento
7. Verificar que documento tiene datos correctos

---

## 📊 Resumen de Tiempo

| Fase | Pasos | Tiempo |
|------|-------|--------|
| 1. Preparación | 1-5 | 30 min |
| 2. Modelos | 6-10 | 30 min |
| 3. Migración | 11-14 | 45 min |
| 4. Endpoints | 15-18 | 45 min |
| 5. Frontend | 19-20 | 30 min |
| **TOTAL** | **20** | **3 horas** |

---

## 🔴 Garantías de Seguridad

### **NO se tocarán:**
- ❌ `cotizaciones` (tabla)
- ❌ `items` (tabla)
- ❌ `documentos` (tabla)
- ❌ `clientes` (tabla)
- ❌ Generadores de documentos existentes
- ❌ Routers de cotizaciones

### **SOLO se modificarán:**
- ✅ `proyectos` (agregar campos nullable)
- ✅ Crear `usuarios` (tabla nueva)
- ✅ Crear routers nuevos (proyectos, usuarios)
- ✅ Actualizar frontend (App.jsx, Chat)

---

## 🎯 Próximo Paso

**¿Procedo con Paso 1 (Verificar BD Actual)?**

Esto solo ejecutará un comando de lectura, sin modificar nada.

**Responde: SÍ o NO**
