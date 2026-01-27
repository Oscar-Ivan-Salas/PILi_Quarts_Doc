from fastapi import APIRouter, HTTPException
from typing import Optional

router = APIRouter(prefix="/api/templates", tags=["templates"])

@router.get("/{template_name}")
async def get_template(template_name: str):
    """
    Retorna el HTML base para una plantilla específica.
    """
    templates = {
        "cotizacion-simple": """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: 'Calibri', sans-serif; color: #333; margin: 40px; }
                .header { border-bottom: 3px solid #D4AF37; padding-bottom: 20px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; }
                .logo { max-width: 150px; }
                .title-container { text-align: right; }
                .title { color: #8B0000; font-size: 28px; font-weight: bold; margin: 0; }
                .meta { color: #666; font-size: 14px; margin-top: 5px; }
                .info-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-bottom: 40px; }
                .info-box h3 { color: #8B0000; border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-bottom: 15px; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th { background-color: #8B0000; color: white; padding: 12px; text-align: left; font-size: 14px; }
                td { padding: 12px; border-bottom: 1px solid #eee; font-size: 14px; }
                .amount { text-align: right; }
                .totals { margin-top: 30px; margin-left: auto; width: 300px; }
                .total-row { display: flex; justify-content: space-between; padding: 8px 0; }
                .total-final { font-weight: bold; font-size: 18px; color: #8B0000; border-top: 2px solid #D4AF37; padding-top: 10px; }
                .footer { margin-top: 60px; font-size: 12px; color: #888; text-align: center; border-top: 1px solid #eee; padding-top: 20px; }
                .conditions { background: #f9f9f9; padding: 15px; border-left: 4px solid #D4AF37; margin-top: 40px; font-size: 13px; }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="logo-container">
                    <!-- LOGO_PLACEHOLDER -->
                    <h1 style="color:#333; margin:0;">PILi<span style="color:#D4AF37">_Quarts</span></h1>
                </div>
                <div class="title-container">
                    <div class="title">COTIZACIÓN</div>
                    <div class="meta">{{NUMERO_COTIZACION}}</div>
                    <div class="meta">{{FECHA_COTIZACION}}</div>
                </div>
            </div>

            <div class="info-grid">
                <div class="info-box">
                    <h3>Cliente</h3>
                    <strong>{{CLIENTE_NOMBRE}}</strong><br>
                    {{PROYECTO_NOMBRE}}
                </div>
                <div class="info-box">
                    <h3>Detalles</h3>
                    <strong>Vigencia:</strong> {{VIGENCIA}}<br>
                    <strong>Normativa:</strong> {{NORMATIVA_APLICABLE}}
                </div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th style="width: 50%">Descripción</th>
                        <th style="width: 15%; text-align: center">Cant.</th>
                        <th style="width: 15%; text-align: right">P. Unit</th>
                        <th style="width: 20%; text-align: right">Total</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{{SERVICIO_NOMBRE}}</td>
                        <td style="text-align: center">1</td>
                         <td class="amount">{{TOTAL}}</td>
                        <td class="amount">{{TOTAL}}</td>
                    </tr>
                   <!-- ITEMS_DYNAMIC_PLACEHOLDER -->
                </tbody>
            </table>

            <div class="totals">
                <div class="total-row">
                    <span>Subtotal:</span>
                    <span>S/ {{SUBTOTAL}}</span>
                </div>
                <div class="total-row">
                    <span>IGV (18%):</span>
                    <span>S/ {{IGV}}</span>
                </div>
                <div class="total-row total-final">
                    <span>Total:</span>
                    <span>S/ {{TOTAL}}</span>
                </div>
            </div>

            <div class="conditions">
                <strong>Condiciones Comerciales:</strong><br>
                - Forma de pago: 50% adelanto, 50% contra entrega.<br>
                - Tiempo de entrega: 5 días hábiles después del adelanto.<br>
                - Precios incluyen IGV salvo indicación contraria.
            </div>

            <div class="footer">
                <strong>PILi_Quarts - Cognitive Document Orchestrator</strong><br>
                Dpto de diseño GatoMichuy huacacayo peru<br>
                ingenieria.teslaelectricidad@gmail.com
            </div>
        </body>
        </html>
        """,
        "proyecto-simple": """<!DOCTYPE html><html><body><h1>Proyecto Simple</h1></body></html>"""
    }

    if template_name not in templates:
        raise HTTPException(status_code=404, detail="Plantilla no encontrada")
    
    return {"html": templates[template_name]}
