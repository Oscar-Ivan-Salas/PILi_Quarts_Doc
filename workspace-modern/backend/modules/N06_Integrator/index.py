import logging
import time
import uuid
from typing import Dict, Any

# Import CLIENT NODES (Allowed only here)
from modules.N02_Pili_Logic.index import logic_node
from modules.N04_Binary_Factory.index import binary_factory

logger = logging.getLogger("N06_Integrator")

class IntegratorNode:
    def dispatch(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrates the circular flow: Frontend -> N02 (Enrich) -> N04 (Generate) -> Frontend
        
        Args:
            request: {
                "client_info": dict,
                "service_request": {
                    "service_key": str,  # e.g., "pozo-tierra"
                    "document_model_id": int, # 1-6
                    "quantity": int      # Global quantity multiplier (default 1)
                },
                "user_context": {
                    "user_id": str,
                    "branding": dict     # Optional
                }
            }
        """
        start_time = time.time()
        log_timings = {}
        
        try:
            # 1. Parsing & Context
            client_info = request.get("client_info", {})
            svc_req = request.get("service_request", {})
            user_ctx = request.get("user_context", {})
            
            service_key = svc_req.get("service_key")
            doc_type_id = svc_req.get("document_model_id", 1)
            quantity = svc_req.get("quantity", 1)
            
            user_id = user_ctx.get("user_id", str(uuid.uuid4()))
            
            # N08 Identity: Branding Extraction
            # Priority: 
            # 1. 'emisor' in root request (from Frontend N08 Form)
            # 2. 'branding' in user_context (Legacy/Direct)
            # 3. Default Tesla Blue
            
            emisor_data = request.get("emisor", {})
            branding_input = user_ctx.get("branding", {})
            
            # Construct Branding Object for N04
            branding = {
                "logo_b64": emisor_data.get("logo") or branding_input.get("logo_b64"),
                "color_hex": emisor_data.get("color_hex") or branding_input.get("color_hex", "#0052A3"),
                "emisor_details": { # Pass full details for templates that need it
                    "nombre": emisor_data.get("nombre"),
                    "ruc": emisor_data.get("ruc"),
                    "direccion": emisor_data.get("direccion"),
                    "firma": emisor_data.get("firma")
                }
            }
            
            logger.info(f"🔄 N06 Dispatch Initiated: {service_key} -> DocType {doc_type_id}")

            # 🌟 V10 MIRROR PROTOCOL INTERCEPTOR 🌟
            if request.get("action") == "generate_matrix_v10":
                logger.info("⚡ V10 Matrix Protocol Activated.")
                # The payload has 'data': {user_id, client_id, project_id}
                # We need to construct a FULL N04 Payload.
                # Simplification: We will use N02 with a dummy service request if needed, 
                # OR if 'data' contains enough info, we use it.
                # Since N02 Enrichment is powerful, we should use it.
                # We force service_key="ELECTRICIDAD" if not provided.
                if not service_key: 
                    service_key = request.get("service", "ELECTRICIDAD")
                
                # Proceed to N02 enrichment as normal, but enforce N04 Dispatch flags
                pass

            # 2. Enrichment (N02 Call)
            t0 = time.time()
            n02_response = logic_node.process_intention({
                "service": service_key,
                "subtype": "*" # We want all items to build the quote
            })
            log_timings["N02_Latency"] = round((time.time() - t0) * 1000, 2)
            
            if not n02_response.get("success"):
                raise Exception(f"N02 Enrichment Failed: {n02_response.get('error')}")
            
            logic_data = n02_response.get("logic_result", {})
            raw_items = logic_data.get("items", [])
            
            if not raw_items:
                logger.warning(f"⚠️ N02 returned 0 items for {service_key}. Using generic fallback or empty.")
            
            # 3. Logic Transformation (N02 -> N04 Format)
            # R.A.L.F: Resolve Template Reference
            available_templates = logic_data.get("templates", {})
            logger.info(f"🔎 N02 Templates: {available_templates} | DocTypeID: {doc_type_id}")
            
            # Try int then str
            template_ref = available_templates.get(doc_type_id)
            if not template_ref:
                template_ref = available_templates.get(str(doc_type_id))
            
            # If not found, fallback to doc_type_id (Legacy or Error)
            # But usually we want to force Universal if template exists.
            target_doc_type = template_ref if template_ref else doc_type_id
            
            # Calculate input for N04
            n04_items = []
            subtotal = 0.0
            
            for item in raw_items:
                # Logic: If item has a specific quantity logic, apply it. 
                # For now, simplistic approach: 1 unit of each * global quantity
                qty = 1 * quantity
                price = item.get("price", 0.0)
                item_total = qty * price
                
                # Base: Copy original N02 item to preserve specific Engineering keys (tablero, prueba, etc.)
                n04_item = item.copy()
                
                # Override/Normalize Standard Commercial Keys
                n04_item.update({
                    "descripcion": item.get("description", item.get("key")),
                    "unidad": item.get("unit", "und"),
                    "cantidad": qty,
                    "precio_unitario": price,
                    # FORMAULA INJECTION for Cuadro de Cargas (ID 3)
                    "total": f"=Product(D{{row}},E{{row}})" if str(target_doc_type) == "3" or str(target_doc_type) == "ELECTRICIDAD_CUADRO_CARGAS" else item_total
                })
                
                n04_items.append(n04_item)
                subtotal += item_total
            
            # Recalculate totals if using formulas? 
            # Subtotal will be wrong if we just sum formula strings.
            # But summary dict expects validation.
            # Ideally N06 keeps the numeric value for 'summary' but sends formula to N04 payload.
            # My current logic puts `n04_items` into payload. 
            # I should use `item_total` for logic accumulation, but `formula` for the payload list.
            # DONE above.
            
            igv = subtotal * 0.18
            total = subtotal + igv
            
            n04_payload = {
                "header": {
                    "user_id": user_id,
                    "service_id": logic_data.get("service_info", {}).get("id", 0),
                    "document_type": target_doc_type # Passes String if found, Int if not
                },
                "branding": {
                    "logo_b64": branding.get("logo_b64"),
                    "color_hex": branding.get("color_hex", "#0052A3")
                },
                "payload": {
                    "items": n04_items,
                    "totals": {
                        "subtotal": round(subtotal, 2),
                        "igv": round(igv, 2),
                        "total": round(total, 2)
                    },
                    "technical_notes": f"Generado automáticamente basado en normativa {logic_data.get('service_info', {}).get('normativa', 'Vigente')}",
                    "client_info": client_info
                },
                # Request ALL 3 formats for Hypothesis Testing if requested
                # But N04 usually takes one format per call? 
                # Contract says 'output_format': str. 
                # For Hypothesis test, the Script calls N06 multiple times or N06 returns multiple?
                # User said "El script debe enviar una orden al Integrador (N06) y recibir los 3 archivos finales."
                # N06 dispatch returns ONE document.
                # So the Script hypothesys_test_N04.py will call N06 3 times or N06 dispatch handles multi-format?
                # Changing N06 to support "ALL" format or list?
                # Let's keep N06 simple (1 format) and let test script loop.
                "output_format": "XLSX" # Default. Integrator input should specify output_format.
            }
            
            # Override format from input request if present
            if "output_format" in request:
                 n04_payload["output_format"] = request["output_format"]

            # 4. Execution (N04 Call)

            # 4. Execution (N04 Call)
            t1 = time.time()
            n04_response = binary_factory.process_request(n04_payload)
            log_timings["N04_Latency"] = round((time.time() - t1) * 1000, 2)
            
            if not n04_response.get("success"):
                raise Exception(f"N04 Generation Failed: {n04_response.get('error')}")

            # 5. Response Construction
            total_time = round((time.time() - start_time) * 1000, 2)
            
            return {
                "success": True,
                "summary": {
                    "message": f"Documento generado exitosamente con {len(n04_items)} items.",
                    "service": service_key,
                    "total_cost": total,
                    "timings_ms": log_timings,
                    "total_process_ms": total_time
                },
                "document": {
                    "url": n04_response.get("filename"), 
                    "b64_preview": n04_response.get("file_b64"), # Full Content for RALF Test
                    "engine": n04_response.get("engine")
                },
                "debug_log": f"N02 Items: {len(raw_items)} | N04 Latency: {log_timings['N04_Latency']}ms"
            }

        except Exception as e:
            logger.error(f"Integrator Failure: {e}", exc_info=True)
            return {
                "success": False, 
                "error": str(e),
                "timings_ms": log_timings
            }

# Singleton
integrator_node = IntegratorNode()
