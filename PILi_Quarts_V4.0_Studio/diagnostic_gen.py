
import sys
import os
import logging
from pathlib import Path

# Setup Path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'backend')))

# Logger to file
logging.basicConfig(
    level=logging.DEBUG,
    filename='DEBUG_GEN.log',
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Diagnostic")

try:
    from modules.N04_Binary_Factory.index import binary_factory
    
    payload = {
        'header': {'service_id': 4, 'user_id': 'DEBUG_USER', 'document_type': 4}, 
        'branding': {'logo_b64': None, 'color_hex': '#0052A3'}, 
        'payload': {
            'client_info': {'nombre': 'TEST'}, 
            'items': [], 
            'totals': {}, 
            'technical_notes': ''
        }, 
        'output_format': 'DOCX'
    }
    
    logger.info("Starting process_request for PROYECTO_COMPLEJO...")
    result = binary_factory.process_request(payload)
    logger.info(f"Result SUCCESS: {result.get('success')}")
    if not result.get('success'):
        logger.error(f"Error: {result.get('error')}")
    
except Exception as e:
    logger.exception("FATAL ERROR IN DIAGNOSTIC:")
