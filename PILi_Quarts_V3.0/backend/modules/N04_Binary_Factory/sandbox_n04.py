import os
import sys
import subprocess
import time
import webbrowser
import logging
from pathlib import Path

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("N04StudioLauncher")

CURRENT_DIR = Path(__file__).parent
STUDIO_DIR = CURRENT_DIR / "studio"

def launch_studio():
    print("-" * 60)
    print("  🎨 N04 MIRROR STUDIO PRO - THE LABORATORY")
    print("-" * 60)
    
    # 1. Iniciar API Backend (Port 8004)
    logger.info("🚀 Iniciando API de Soberanía (Backend)...")
    api_process = subprocess.Popen(
        [sys.executable, str(CURRENT_DIR / "studio_api.py")],
        cwd=str(CURRENT_DIR)
    )
    
    # Pequeña espera para que la API asiente
    time.sleep(2)
    
    # 2. Iniciar Frontend Vite (Port 5173)
    logger.info("✨ Iniciando Frontend Studio (Vite)...")
    try:
        # Usamos shell=True para Windows y asegurar que encuentre npm
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=str(STUDIO_DIR),
            shell=True
        )
    except Exception as e:
        logger.error(f"❌ Error iniciando frontend: {e}")
        api_process.terminate()
        return

    # 3. Abrir Navegador
    time.sleep(5)
    logger.info("🌍 Abriendo Mirror Studio en http://localhost:5173")
    webbrowser.open("http://localhost:5173")
    
    print("\n" + "="*60)
    print(" LABORATORIO ACTIVO: http://localhost:5173")
    print(" Presiona Ctrl+C para apagar el sistema.")
    print("="*60 + "\n")
    
    try:
        while True:
            time.sleep(1)
            if api_process.poll() is not None:
                logger.error("🛑 La API se ha detenido inesperadamente.")
                break
            if frontend_process.poll() is not None:
                logger.error("🛑 El Frontend se ha detenido inesperadamente.")
                break
    except KeyboardInterrupt:
        logger.info("\n🛑 Apagando Laboratorio...")
    finally:
        api_process.terminate()
        # En Windows a veces hay que matar el árbol de procesos de npm
        try:
            if sys.platform == "win32":
                subprocess.call(['taskkill', '/F', '/T', '/PID', str(frontend_process.pid)])
            else:
                frontend_process.terminate()
        except:
            pass
        logger.info("✅ Laboratorio cerrado correctamente.")

if __name__ == "__main__":
    launch_studio()
