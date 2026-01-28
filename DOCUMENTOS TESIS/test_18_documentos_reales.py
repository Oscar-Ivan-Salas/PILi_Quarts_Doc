#!/usr/bin/env python3
"""
Script de prueba REAL - 18 documentos profesionales
Simula comportamiento de usuario real generando 3 documentos de cada tipo
con datos variados y realistas
"""
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Agregar backend al path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app.services.html_to_word_generator import html_to_word_generator

# Directorio de salida
OUTPUT_DIR = Path(__file__).parent / "storage" / "generados"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("🎯 PRUEBA REAL - 18 DOCUMENTOS PROFESIONALES COMO USUARIO REAL")
print("=" * 80)
print(f"📁 Directorio salida: {OUTPUT_DIR}")
print(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
print(f"👤 Simulando comportamiento de usuario real de Tesla Electricidad")
print("=" * 80)
print()

resultados = []
contador = 0

# ═══════════════════════════════════════════════════════════════════
# COTIZACIONES SIMPLES (3 documentos)
# ═══════════════════════════════════════════════════════════════════
print("📋 GRUPO 1/6: COTIZACIONES SIMPLES (3 documentos)")
print("-" * 80)

cotizaciones_simples = [
    {
        "nombre": "Oficina Administrativa",
        "datos": {
            "numero": "COT-202512-0001",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "cliente": "CORPORACIÓN INDUSTRIAL ABC S.A.C.",
            "proyecto": "Instalación Eléctrica Oficinas Administrativas - Piso 3",
            "atencion": "Ing. Carlos Mendoza - Gerente de Operaciones",
            "items": [
                {"descripcion": "Tablero eléctrico general 3F 100A con accesorios", "cantidad": 1, "unidad": "und", "precio_unitario": 1200.00},
                {"descripcion": "Cable THW 10mm² - Color Rojo (Fase)", "cantidad": 50, "unidad": "m", "precio_unitario": 3.80},
                {"descripcion": "Cable THW 10mm² - Color Negro (Fase)", "cantidad": 50, "unidad": "m", "precio_unitario": 3.80},
                {"descripcion": "Cable THW 10mm² - Color Azul (Neutro)", "cantidad": 50, "unidad": "m", "precio_unitario": 3.80},
                {"descripcion": "Luminaria LED panel empotrable 60x60 48W luz fría", "cantidad": 20, "unidad": "und", "precio_unitario": 85.00},
                {"descripcion": "Tomacorriente doble empotrable con línea a tierra", "cantidad": 30, "unidad": "und", "precio_unitario": 12.50},
                {"descripcion": "Interruptor termomagnético 2x32A Schneider Electric", "cantidad": 8, "unidad": "und", "precio_unitario": 45.00},
                {"descripcion": "Tubería PVC-P liviana 3/4\" x 3m", "cantidad": 15, "unidad": "und", "precio_unitario": 8.50},
            ],
            "observaciones": "Precios en Soles peruanos incluyen IGV. Instalación según CNE-Utilización 2011. Incluye materiales, mano de obra y pruebas.",
            "vigencia": "30 días calendario"
        }
    },
    {
        "nombre": "Tienda Comercial",
        "datos": {
            "numero": "COT-202512-0002",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "cliente": "COMERCIAL LOS ANDES E.I.R.L.",
            "proyecto": "Sistema Eléctrico Tienda Comercial - Av. Real 234",
            "atencion": "Sr. Roberto Flores - Propietario",
            "items": [
                {"descripcion": "Tablero eléctrico monofásico 60A", "cantidad": 1, "unidad": "und", "precio_unitario": 650.00},
                {"descripcion": "Cable NYY 3x6mm² subterráneo", "cantidad": 30, "unidad": "m", "precio_unitario": 12.50},
                {"descripcion": "Reflector LED 50W para exteriores", "cantidad": 4, "unidad": "und", "precio_unitario": 75.00},
                {"descripcion": "Luminaria LED tubular 18W 60cm", "cantidad": 12, "unidad": "und", "precio_unitario": 28.00},
                {"descripcion": "Tomacorriente doble universal empotrable", "cantidad": 15, "unidad": "und", "precio_unitario": 11.00},
                {"descripcion": "Interruptor simple empotrable", "cantidad": 8, "unidad": "und", "precio_unitario": 6.50},
                {"descripcion": "Caja de paso metálica 10x10x5 cm", "cantidad": 6, "unidad": "und", "precio_unitario": 15.00},
            ],
            "observaciones": "Incluye IGV. Garantía de 12 meses en materiales eléctricos. Instalación en horario comercial.",
            "vigencia": "20 días calendario"
        }
    },
    {
        "nombre": "Vivienda Unifamiliar",
        "datos": {
            "numero": "COT-202512-0003",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "cliente": "FAMILIA GARCÍA TORRES",
            "proyecto": "Instalación Eléctrica Vivienda Unifamiliar - Urb. Los Pinos",
            "atencion": "Sr. Miguel García",
            "items": [
                {"descripcion": "Tablero eléctrico residencial 3F 60A", "cantidad": 1, "unidad": "und", "precio_unitario": 850.00},
                {"descripcion": "Cable TW 8mm² para circuito cocina", "cantidad": 25, "unidad": "m", "precio_unitario": 5.20},
                {"descripcion": "Cable TW 4mm² para circuitos de tomacorrientes", "cantidad": 80, "unidad": "m", "precio_unitario": 2.80},
                {"descripcion": "Cable TW 2.5mm² para circuitos de iluminación", "cantidad": 100, "unidad": "m", "precio_unitario": 1.90},
                {"descripcion": "Luminaria LED decorativa 12W sala/comedor", "cantidad": 8, "unidad": "und", "precio_unitario": 45.00},
                {"descripcion": "Luminaria LED 9W dormitorios", "cantidad": 12, "unidad": "und", "precio_unitario": 25.00},
                {"descripcion": "Tomacorriente doble empotrable línea Premium", "cantidad": 25, "unidad": "und", "precio_unitario": 14.00},
                {"descripcion": "Interruptor conmutador doble", "cantidad": 6, "unidad": "und", "precio_unitario": 12.00},
                {"descripcion": "Pozo a tierra completo (varilla, sales, soldadura)", "cantidad": 1, "unidad": "glb", "precio_unitario": 450.00},
            ],
            "observaciones": "Precios incluyen IGV. Sistema según CNE vigente. Garantía 18 meses.",
            "vigencia": "25 días calendario"
        }
    }
]

for i, cot in enumerate(cotizaciones_simples, 1):
    print(f"📄 {contador+1}/18: Generando Cotización Simple {i} - {cot['nombre']}...")
    try:
        ruta = OUTPUT_DIR / f"COT_SIMPLE_{i}_{cot['nombre'].replace(' ', '_').upper()}.docx"
        html_to_word_generator.generar_cotizacion_simple(cot["datos"], ruta)
        size_kb = ruta.stat().st_size / 1024
        print(f"   ✅ Generado: {ruta.name} ({size_kb:.1f} KB)")
        resultados.append((f"Cotización Simple {i}", True, ruta, size_kb))
        contador += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        resultados.append((f"Cotización Simple {i}", False, None, 0))
        contador += 1

print()

# ═══════════════════════════════════════════════════════════════════
# COTIZACIONES COMPLEJAS (3 documentos)
# ═══════════════════════════════════════════════════════════════════
print("📋 GRUPO 2/6: COTIZACIONES COMPLEJAS (3 documentos)")
print("-" * 80)

cotizaciones_complejas = [
    {
        "nombre": "Edificio Corporativo",
        "datos": {
            "numero": "COT-202512-0004-PRO",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "cliente": "CONSTRUCTORA MEGAPROYECTOS S.A.",
            "proyecto": "Sistema Eléctrico Integral Edificio Corporativo Torre Azul - 8 Pisos",
            "atencion": "Arq. Patricia Rojas - Gerente de Proyectos / Ing. Luis Campos - Supervisor Eléctrico",
            "items": [
                {"descripcion": "Subestación eléctrica 630 kVA (transformador, celdas MT, protecciones)", "cantidad": 1, "unidad": "und", "precio_unitario": 45000.00},
                {"descripcion": "Tablero de distribución general 3F 800A con medición digital", "cantidad": 2, "unidad": "und", "precio_unitario": 8500.00},
                {"descripcion": "Tableros de piso (8 tableros, uno por piso)", "cantidad": 8, "unidad": "und", "precio_unitario": 2800.00},
                {"descripcion": "Sistema de puesta a tierra (pozo a tierra completo con medición)", "cantidad": 1, "unidad": "glb", "precio_unitario": 3500.00},
                {"descripcion": "Cable NYY 3x70mm² + 35mm² (tierra) - Alimentador principal", "cantidad": 250, "unidad": "m", "precio_unitario": 28.50},
                {"descripcion": "Cable NYY 3x25mm² + 16mm² - Alimentadores secundarios", "cantidad": 400, "unidad": "m", "precio_unitario": 15.80},
                {"descripcion": "Luminarias LED panel empotrable 60x60 48W oficinas", "cantidad": 80, "unidad": "und", "precio_unitario": 85.00},
                {"descripcion": "Luminarias LED downlight 18W pasillos", "cantidad": 60, "unidad": "und", "precio_unitario": 45.00},
                {"descripcion": "Sistema detección y alarma contra incendios (8 pisos)", "cantidad": 1, "unidad": "glb", "precio_unitario": 12000.00},
                {"descripcion": "Sistema de iluminación de emergencia", "cantidad": 1, "unidad": "glb", "precio_unitario": 5500.00},
            ],
            "condiciones": "Instalación certificada según CNE Suministro y Utilización 2011. Incluye pruebas de protocolo, medición de puesta a tierra, termografía y puesta en marcha supervisada. Materiales de primera calidad con certificaciones internacionales.",
            "terminos_pago": "40% adelanto, 40% avance 50% de obra, 20% contra entrega final y conformidad",
            "garantia_meses": "24 meses en materiales y mano de obra",
            "vigencia": "45 días calendario"
        }
    },
    {
        "nombre": "Centro Comercial",
        "datos": {
            "numero": "COT-202512-0005-PRO",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "cliente": "INVERSIONES PLAZA NORTE S.A.C.",
            "proyecto": "Sistema Eléctrico y Contra Incendios Centro Comercial Plaza Norte - 3 Niveles",
            "atencion": "Ing. Sandra Vega - Jefe de Proyectos",
            "items": [
                {"descripcion": "Subestación eléctrica 1000 kVA trifásica", "cantidad": 1, "unidad": "und", "precio_unitario": 65000.00},
                {"descripcion": "Tablero general de distribución 1200A", "cantidad": 1, "unidad": "und", "precio_unitario": 15000.00},
                {"descripcion": "Grupo electrógeno 200 kVA (emergencia)", "cantidad": 1, "unidad": "und", "precio_unitario": 38000.00},
                {"descripcion": "Sistema de transferencia automática", "cantidad": 1, "unidad": "und", "precio_unitario": 8500.00},
                {"descripcion": "Cable NYY 4x120mm² + 70mm² - Alimentador general", "cantidad": 180, "unidad": "m", "precio_unitario": 48.00},
                {"descripcion": "Luminarias LED comerciales 36W", "cantidad": 150, "unidad": "und", "precio_unitario": 95.00},
                {"descripcion": "Sistema contra incendios (detectores, rociadores, bombas)", "cantidad": 1, "unidad": "glb", "precio_unitario": 45000.00},
                {"descripcion": "Sistema de iluminación de emergencia y señalética", "cantidad": 1, "unidad": "glb", "precio_unitario": 12000.00},
                {"descripcion": "Cableado estructurado CAT6A para red", "cantidad": 1, "unidad": "glb", "precio_unitario": 18000.00},
            ],
            "condiciones": "Obra incluye ingeniería de detalle, suministro, instalación y puesta en marcha. Cumple normativa NFPA 72 y CNE vigente. Incluye capacitación al personal de mantenimiento.",
            "terminos_pago": "30% adelanto, 30% aprobación de ingeniería, 30% avance 60%, 10% entrega final",
            "garantia_meses": "36 meses en equipos, 24 meses en instalación",
            "vigencia": "60 días calendario"
        }
    },
    {
        "nombre": "Planta Industrial",
        "datos": {
            "numero": "COT-202512-0006-PRO",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "cliente": "INDUSTRIAS TEXTILES PREMIUM S.A.C.",
            "proyecto": "Modernización Sistema Eléctrico Planta Industrial - Zona Producción",
            "atencion": "Ing. Ricardo Salazar - Jefe de Mantenimiento / Ing. Ana Gutiérrez - Gerente Producción",
            "items": [
                {"descripcion": "Subestación eléctrica 800 kVA con seccionador", "cantidad": 1, "unidad": "und", "precio_unitario": 52000.00},
                {"descripcion": "Centro de control de motores (CCM) 480V", "cantidad": 1, "unidad": "und", "precio_unitario": 28000.00},
                {"descripcion": "Variadores de frecuencia 75 HP", "cantidad": 4, "unidad": "und", "precio_unitario": 6500.00},
                {"descripcion": "Banco de condensadores automático 150 kVAR", "cantidad": 1, "unidad": "und", "precio_unitario": 12000.00},
                {"descripcion": "Cable NYY 4x95mm² + 50mm² - Alimentadores", "cantidad": 300, "unidad": "m", "precio_unitario": 38.00},
                {"descripcion": "Luminarias LED industriales 150W antiexplosivas", "cantidad": 45, "unidad": "und", "precio_unitario": 280.00},
                {"descripcion": "Sistema de medición y monitoreo de energía", "cantidad": 1, "unidad": "glb", "precio_unitario": 15000.00},
                {"descripcion": "Puesta a tierra industrial con múltiples pozos", "cantidad": 1, "unidad": "glb", "precio_unitario": 8500.00},
            ],
            "condiciones": "Instalación con mínima interrupción de producción (trabajo nocturno/fines de semana). Certificaciones de calidad ISO. Incluye estudios de factor de potencia y análisis de armónicos.",
            "terminos_pago": "35% adelanto, 35% avance 50%, 30% puesta en marcha exitosa",
            "garantia_meses": "30 meses en equipos electrónicos, 24 meses en instalación",
            "vigencia": "50 días calendario"
        }
    }
]

for i, cot in enumerate(cotizaciones_complejas, 1):
    print(f"📄 {contador+1}/18: Generando Cotización Compleja {i} - {cot['nombre']}...")
    try:
        ruta = OUTPUT_DIR / f"COT_COMPLEJA_{i}_{cot['nombre'].replace(' ', '_').upper()}.docx"
        html_to_word_generator.generar_cotizacion_compleja(cot["datos"], ruta)
        size_kb = ruta.stat().st_size / 1024
        print(f"   ✅ Generado: {ruta.name} ({size_kb:.1f} KB)")
        resultados.append((f"Cotización Compleja {i}", True, ruta, size_kb))
        contador += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        resultados.append((f"Cotización Compleja {i}", False, None, 0))
        contador += 1

print()

# ═══════════════════════════════════════════════════════════════════
# PROYECTOS SIMPLES (3 documentos)
# ═══════════════════════════════════════════════════════════════════
print("📋 GRUPO 3/6: PROYECTOS SIMPLES (3 documentos)")
print("-" * 80)

proyectos_simples = [
    {
        "nombre": "Modernización Industrial",
        "datos": {
            "nombre": "Modernización Sistema Eléctrico Planta Industrial Huancayo",
            "codigo": "PROY-202512-001",
            "cliente": "INDUSTRIAS METALMECÁNICAS DEL SUR S.A.C.",
            "fecha_inicio": "15/01/2025",
            "fecha_fin": "15/03/2025",
            "duracion_total": "60 días calendario",
            "presupuesto": 85000.00,
            "alcance": "Modernización completa del sistema eléctrico de planta industrial incluyendo: subestación eléctrica 500 kVA, tableros de distribución de última generación, sistema de iluminación LED industrial, puesta a tierra certificada y sistema de monitoreo energético. El proyecto contempla trabajo sin detener producción (horarios nocturnos y fines de semana).",
            "normativa": "CNE Suministro 2011, CNE Utilización 2011, NTP-IEC 60364-1, NFPA 70E"
        }
    },
    {
        "nombre": "Certificación ITSE",
        "datos": {
            "nombre": "Implementación Sistema Eléctrico para Certificado ITSE - Restaurante",
            "codigo": "PROY-202512-002",
            "cliente": "CORPORACIÓN GASTRONÓMICA LA MESA PERUANA S.A.C.",
            "fecha_inicio": "05/02/2025",
            "fecha_fin": "25/02/2025",
            "duracion_total": "20 días calendario",
            "presupuesto": 28000.00,
            "alcance": "Implementación de sistema eléctrico conforme a requerimientos ITSE para local de restaurante de 250 m². Incluye: tablero general normalizado, circuitos independientes cocina, iluminación LED de emergencia, sistema contra incendios básico (detectores de humo), puesta a tierra certificada, planos conforme a obra y memoria descriptiva para ITSE.",
            "normativa": "CNE Utilización 2011, Reglamento Nacional de Edificaciones, INDECI Certificado ITSE"
        }
    },
    {
        "nombre": "Ampliación Educativa",
        "datos": {
            "nombre": "Instalación Eléctrica Pabellón Educativo - Colegio San José",
            "codigo": "PROY-202512-003",
            "cliente": "INSTITUCIÓN EDUCATIVA PRIVADA SAN JOSÉ",
            "fecha_inicio": "10/01/2025",
            "fecha_fin": "05/02/2025",
            "duracion_total": "25 días calendario",
            "presupuesto": 45000.00,
            "alcance": "Instalación eléctrica completa para nuevo pabellón educativo de 3 pisos (12 aulas, laboratorio, sala de cómputo). Incluye: tablero general trifásico, tableros por piso, iluminación LED en todas las aulas, sistema de tomacorrientes de seguridad, circuitos independientes para equipos de cómputo, iluminación de emergencia y puesta a tierra educativa.",
            "normativa": "CNE Utilización 2011, RNE - Norma A.040 Educación, MINEDU"
        }
    }
]

for i, proy in enumerate(proyectos_simples, 1):
    print(f"📄 {contador+1}/18: Generando Proyecto Simple {i} - {proy['nombre']}...")
    try:
        ruta = OUTPUT_DIR / f"PROY_SIMPLE_{i}_{proy['nombre'].replace(' ', '_').upper()}.docx"
        html_to_word_generator.generar_proyecto_simple(proy["datos"], ruta)
        size_kb = ruta.stat().st_size / 1024
        print(f"   ✅ Generado: {ruta.name} ({size_kb:.1f} KB)")
        resultados.append((f"Proyecto Simple {i}", True, ruta, size_kb))
        contador += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        resultados.append((f"Proyecto Simple {i}", False, None, 0))
        contador += 1

print()

# ═══════════════════════════════════════════════════════════════════
# PROYECTOS COMPLEJOS PMI (3 documentos)
# ═══════════════════════════════════════════════════════════════════
print("📋 GRUPO 4/6: PROYECTOS COMPLEJOS PMI (3 documentos)")
print("-" * 80)

proyectos_pmi = [
    {
        "nombre": "Automatización Minera",
        "datos": {
            "nombre": "Implementación Sistema SCADA y Automatización Industrial - Mina Atlas",
            "codigo": "PROY-202512-004-PMI",
            "cliente": "CORPORACIÓN MINERA ATLAS S.A.C.",
            "fecha_inicio": "01/02/2025",
            "fecha_fin": "01/08/2025",
            "duracion_total": "180 días calendario",
            "presupuesto": 350000.00,
            "alcance": "Project Charter PMI para implementación completa de sistema SCADA, automatización de procesos productivos mineros, sistema eléctrico de respaldo con UPS industrial, monitoreo remoto 24/7 y capacitación especializada. Incluye gestión integral según PMBoK 7th Edition con entregables por fases.",
            "normativa": "PMBoK 7th Edition, CNE Suministro 2011, IEC 61508, ISO 9001:2015",
            "spi": "1.05",
            "cpi": "0.98",
            "ev": 175000,
            "pv": 166667,
            "ac": 178571,
            "dias_ingenieria": "45",
            "dias_ejecucion": "120"
        }
    },
    {
        "nombre": "Hospital Regional",
        "datos": {
            "nombre": "Sistema Eléctrico y Emergencia Hospital Regional Huancayo - PMI",
            "codigo": "PROY-202512-005-PMI",
            "cliente": "MINISTERIO DE SALUD - DIRESA JUNÍN",
            "fecha_inicio": "15/01/2025",
            "fecha_fin": "15/10/2025",
            "duracion_total": "270 días calendario",
            "presupuesto": 850000.00,
            "alcance": "Proyecto de inversión pública bajo metodología PMI para implementación de sistema eléctrico hospitalario con redundancia completa: subestaciones eléctricas gemelas 1250 kVA, grupos electrógenos 500 kVA con transferencia automática, UPS hospitalaria 200 kVA, sistema de emergencia normativo para quirófanos y UCI, iluminación quirúrgica especializada, puesta a tierra hospitalaria según norma.",
            "normativa": "PMBoK 7th Edition, NTS Nº 113-MINSA (Infraestructura Hospitalaria), CNE, NFPA 99",
            "spi": "1.02",
            "cpi": "1.08",
            "ev": 425000,
            "pv": 416667,
            "ac": 393518,
            "dias_ingenieria": "60",
            "dias_ejecucion": "180"
        }
    },
    {
        "nombre": "Data Center",
        "datos": {
            "nombre": "Implementación Data Center Tier III - Infraestructura Crítica PMI",
            "codigo": "PROY-202512-006-PMI",
            "cliente": "BANCO CONTINENTAL DEL PERÚ",
            "fecha_inicio": "01/03/2025",
            "fecha_fin": "01/12/2025",
            "duracion_total": "270 días calendario",
            "presupuesto": 1200000.00,
            "alcance": "Project Charter PMI para Data Center Tier III bancario: doble subestación eléctrica 800 kVA (N+1), grupos electrógenos paralelo 600 kVA, sistema UPS redundante 400 kVA (2N), PDUs inteligentes, climatización de precisión, monitoreo DCIM, sistema contra incendios FM-200, control de acceso biométrico, cableado estructurado CAT6A/fibra óptica. Gestión PMI con oficina de proyecto dedicada.",
            "normativa": "PMBoK 7th Edition, TIA-942 Tier III, Uptime Institute, ISO 27001, PCI-DSS",
            "spi": "0.98",
            "cpi": "0.96",
            "ev": 600000,
            "pv": 612244,
            "ac": 625000,
            "dias_ingenieria": "90",
            "dias_ejecucion": "150"
        }
    }
]

for i, proy in enumerate(proyectos_pmi, 1):
    print(f"📄 {contador+1}/18: Generando Proyecto PMI {i} - {proy['nombre']}...")
    try:
        ruta = OUTPUT_DIR / f"PROY_PMI_{i}_{proy['nombre'].replace(' ', '_').upper()}.docx"
        html_to_word_generator.generar_proyecto_complejo(proy["datos"], ruta)
        size_kb = ruta.stat().st_size / 1024
        print(f"   ✅ Generado: {ruta.name} ({size_kb:.1f} KB)")
        resultados.append((f"Proyecto PMI {i}", True, ruta, size_kb))
        contador += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        resultados.append((f"Proyecto PMI {i}", False, None, 0))
        contador += 1

print()

# ═══════════════════════════════════════════════════════════════════
# INFORMES TÉCNICOS (3 documentos)
# ═══════════════════════════════════════════════════════════════════
print("📋 GRUPO 5/6: INFORMES TÉCNICOS (3 documentos)")
print("-" * 80)

informes_tecnicos = [
    {
        "nombre": "Puesta Tierra Corporativo",
        "datos": {
            "titulo": "Informe Técnico: Sistema de Puesta a Tierra - Edificio Corporativo Banco Continental",
            "codigo": "INF-TEC-202512-001",
            "cliente": "BANCO CONTINENTAL DEL PERÚ",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "servicio_nombre": "Implementación y Certificación Sistema Puesta a Tierra según CNE",
            "resumen": "El presente informe técnico describe el diseño, instalación, pruebas y certificación del sistema de puesta a tierra implementado en el Edificio Corporativo del Banco Continental, sede Lima. El sistema cumple con CNE Suministro 2011 y garantiza resistencia menor a 5 ohmios según mediciones protocolizadas.",
            "normativa": "CNE Suministro 2011, NTP-IEC 60364-5-54, IEEE Std 142-2007"
        }
    },
    {
        "nombre": "Certificación ITSE Hotel",
        "datos": {
            "titulo": "Informe Técnico: Certificado ITSE - Sistema Eléctrico y Contra Incendios Hotel Turístico",
            "codigo": "INF-TEC-202512-002",
            "cliente": "INVERSIONES HOTELERAS PREMIUM S.A.C.",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "servicio_nombre": "Implementación Sistema Eléctrico y Contra Incendios para ITSE",
            "resumen": "Informe técnico que detalla la implementación del sistema eléctrico y contra incendios del Hotel Turístico Premium (120 habitaciones) conforme a requisitos INDECI para obtención de Certificado ITSE. Incluye memoria descriptiva, planos conforme a obra, protocolos de prueba y certificados de conformidad de todos los equipos instalados.",
            "normativa": "CNE Utilización 2011, NFPA 72, Reglamento Nacional de Edificaciones A.030, D.S. 002-2018-PCM"
        }
    },
    {
        "nombre": "Auditoria Industrial",
        "datos": {
            "titulo": "Informe Técnico: Auditoría Eléctrica Planta Industrial - Detección Puntos Críticos",
            "codigo": "INF-TEC-202512-003",
            "cliente": "INDUSTRIAS ALIMENTARIAS DEL CENTRO S.A.C.",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "servicio_nombre": "Auditoría Integral Sistema Eléctrico Industrial",
            "resumen": "Auditoría técnica exhaustiva del sistema eléctrico de planta industrial de alimentos, incluyendo: termografía infrarroja de tableros y conexiones, medición de calidad de energía, análisis de factor de potencia, inspección visual de instalaciones, medición de puestas a tierra y recomendaciones de mejora. Se identificaron 15 puntos críticos que requieren intervención inmediata por riesgo de incendio.",
            "normativa": "CNE Suministro 2011, NFPA 70B, ISO 50001 (Gestión Energética)"
        }
    }
]

for i, inf in enumerate(informes_tecnicos, 1):
    print(f"📄 {contador+1}/18: Generando Informe Técnico {i} - {inf['nombre']}...")
    try:
        ruta = OUTPUT_DIR / f"INF_TECNICO_{i}_{inf['nombre'].replace(' ', '_').upper()}.docx"
        html_to_word_generator.generar_informe_tecnico(inf["datos"], ruta)
        size_kb = ruta.stat().st_size / 1024
        print(f"   ✅ Generado: {ruta.name} ({size_kb:.1f} KB)")
        resultados.append((f"Informe Técnico {i}", True, ruta, size_kb))
        contador += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        resultados.append((f"Informe Técnico {i}", False, None, 0))
        contador += 1

print()

# ═══════════════════════════════════════════════════════════════════
# INFORMES EJECUTIVOS APA (3 documentos)
# ═══════════════════════════════════════════════════════════════════
print("📋 GRUPO 6/6: INFORMES EJECUTIVOS APA (3 documentos)")
print("-" * 80)

informes_ejecutivos = [
    {
        "nombre": "Viabilidad Textil",
        "datos": {
            "titulo": "Informe Ejecutivo APA: Viabilidad Económica Modernización Energética - Textiles Premium",
            "codigo": "INF-EXE-202512-001-APA",
            "cliente": "TEXTILES PERUANOS PREMIUM S.A.C.",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "servicio_nombre": "Estudio de Viabilidad Técnico-Económica Modernización Sistema Eléctrico",
            "resumen": "El presente informe ejecutivo, elaborado bajo normas APA 7th Edition, analiza la viabilidad técnica y económica del proyecto de modernización del sistema eléctrico de Textiles Peruanos Premium. Incluye análisis financiero detallado con proyecciones a 5 años, cálculo de retorno de inversión (ROI 28%), evaluación de ahorro energético estimado en 35% anual y recomendaciones estratégicas para implementación por fases.",
            "presupuesto": 180000.00,
            "roi": "28",
            "payback": "16",
            "tir": "32",
            "ahorro_anual": 42000,
            "ahorro_energetico": 85000,
            "normativa": "CNE Suministro 2011, ISO 50001:2018 (Gestión Energética), NTP-IEC 60364"
        }
    },
    {
        "nombre": "Inversión Minera",
        "datos": {
            "titulo": "Informe Ejecutivo APA: Análisis Costo-Beneficio Implementación SCADA Minero",
            "codigo": "INF-EXE-202512-002-APA",
            "cliente": "CORPORACIÓN MINERA ATLAS S.A.C.",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "servicio_nombre": "Estudio Financiero Implementación Sistema SCADA Industrial",
            "resumen": "Estudio ejecutivo formato APA que evalúa la inversión en sistema SCADA para automatización de procesos mineros. Análisis incluye: proyección de incremento de productividad (22%), reducción de costos operativos (18%), mejora en seguridad operacional, retorno de inversión calculado en 24 meses, TIR del 38% y recomendaciones de implementación según mejores prácticas PMI.",
            "presupuesto": 350000.00,
            "roi": "35",
            "payback": "24",
            "tir": "38",
            "ahorro_anual": 130000,
            "ahorro_energetico": 210000,
            "normativa": "PMBoK 7th Edition, IEC 61508 (Seguridad Funcional), ISO 9001:2015"
        }
    },
    {
        "nombre": "Hospital Inversión",
        "datos": {
            "titulo": "Informe Ejecutivo APA: Justificación Inversión Sistema Eléctrico Hospitalario - Análisis Social",
            "codigo": "INF-EXE-202512-003-APA",
            "cliente": "MINISTERIO DE SALUD - DIRESA JUNÍN",
            "fecha": datetime.now().strftime("%d/%m/%Y"),
            "servicio_nombre": "Estudio de Inversión Pública - Sistema Eléctrico Hospital Regional",
            "resumen": "Informe ejecutivo académico formato APA 7th para sustentación de inversión pública en sistema eléctrico hospitalario. Incluye: análisis de impacto social (atención 150,000 pacientes/año), evaluación económica con metodología SNIP, cálculo de beneficios sociales cuantificables, análisis de riesgo, sostenibilidad operativa y conclusiones con evidencia científica. Inversión socialmente rentable con indicadores VAN social positivo.",
            "presupuesto": 850000.00,
            "roi": "18",
            "payback": "36",
            "tir": "22",
            "ahorro_anual": 95000,
            "ahorro_energetico": 180000,
            "normativa": "NTS Nº 113-MINSA, Sistema Nacional de Inversión Pública, PMBoK 7th, NFPA 99"
        }
    }
]

for i, inf in enumerate(informes_ejecutivos, 1):
    print(f"📄 {contador+1}/18: Generando Informe Ejecutivo APA {i} - {inf['nombre']}...")
    try:
        ruta = OUTPUT_DIR / f"INF_EJECUTIVO_{i}_{inf['nombre'].replace(' ', '_').upper()}.docx"
        html_to_word_generator.generar_informe_ejecutivo(inf["datos"], ruta)
        size_kb = ruta.stat().st_size / 1024
        print(f"   ✅ Generado: {ruta.name} ({size_kb:.1f} KB)")
        resultados.append((f"Informe Ejecutivo {i}", True, ruta, size_kb))
        contador += 1
    except Exception as e:
        print(f"   ❌ Error: {e}")
        resultados.append((f"Informe Ejecutivo {i}", False, None, 0))
        contador += 1

print()

# ═══════════════════════════════════════════════════════════════════
# RESUMEN FINAL
# ═══════════════════════════════════════════════════════════════════
print("=" * 80)
print("📊 RESUMEN COMPLETO DE GENERACIÓN")
print("=" * 80)

exitosos = sum(1 for _, exito, _, _ in resultados if exito)
total = len(resultados)

print(f"\n🎯 GRUPO 1: COTIZACIONES SIMPLES (3 docs)")
print("-" * 80)
for i, (nombre, exito, ruta, size) in enumerate(resultados[0:3]):
    status = "✅" if exito else "❌"
    if exito:
        print(f"{status} {nombre:35} → {ruta.name:50} ({size:.1f} KB)")
    else:
        print(f"{status} {nombre:35} → ERROR")

print(f"\n📋 GRUPO 2: COTIZACIONES COMPLEJAS (3 docs)")
print("-" * 80)
for i, (nombre, exito, ruta, size) in enumerate(resultados[3:6]):
    status = "✅" if exito else "❌"
    if exito:
        print(f"{status} {nombre:35} → {ruta.name:50} ({size:.1f} KB)")
    else:
        print(f"{status} {nombre:35} → ERROR")

print(f"\n🏗️ GRUPO 3: PROYECTOS SIMPLES (3 docs)")
print("-" * 80)
for i, (nombre, exito, ruta, size) in enumerate(resultados[6:9]):
    status = "✅" if exito else "❌"
    if exito:
        print(f"{status} {nombre:35} → {ruta.name:50} ({size:.1f} KB)")
    else:
        print(f"{status} {nombre:35} → ERROR")

print(f"\n🎯 GRUPO 4: PROYECTOS PMI (3 docs)")
print("-" * 80)
for i, (nombre, exito, ruta, size) in enumerate(resultados[9:12]):
    status = "✅" if exito else "❌"
    if exito:
        print(f"{status} {nombre:35} → {ruta.name:50} ({size:.1f} KB)")
    else:
        print(f"{status} {nombre:35} → ERROR")

print(f"\n📄 GRUPO 5: INFORMES TÉCNICOS (3 docs)")
print("-" * 80)
for i, (nombre, exito, ruta, size) in enumerate(resultados[12:15]):
    status = "✅" if exito else "❌"
    if exito:
        print(f"{status} {nombre:35} → {ruta.name:50} ({size:.1f} KB)")
    else:
        print(f"{status} {nombre:35} → ERROR")

print(f"\n📊 GRUPO 6: INFORMES EJECUTIVOS APA (3 docs)")
print("-" * 80)
for i, (nombre, exito, ruta, size) in enumerate(resultados[15:18]):
    status = "✅" if exito else "❌"
    if exito:
        print(f"{status} {nombre:35} → {ruta.name:50} ({size:.1f} KB)")
    else:
        print(f"{status} {nombre:35} → ERROR")

print("\n" + "=" * 80)
print(f"🎯 TOTAL: {exitosos}/{total} documentos generados correctamente")
print(f"📁 Ubicación: {OUTPUT_DIR}")
print("=" * 80)

# Tamaño total
tamanio_total = sum(size for _, exito, _, size in resultados if exito)
print(f"💾 Tamaño total: {tamanio_total:.1f} KB ({tamanio_total/1024:.2f} MB)")

if exitosos == total:
    print("\n🎉 ¡ÉXITO TOTAL! Todos los 18 documentos se generaron correctamente")
    print("✨ Sistema 100% funcional con casos de uso reales")
    sys.exit(0)
else:
    print(f"\n⚠️  ATENCIÓN: {total - exitosos} documentos no se generaron")
    sys.exit(1)
