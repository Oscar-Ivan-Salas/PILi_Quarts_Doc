#!/bin/bash
# N04 Binary Factory - Script de arranque Linux/Servidor
# Backend: http://0.0.0.0:8005
# Frontend: http://0.0.0.0:5173

echo "============================================"
echo "  N04 BINARY FACTORY - STUDIO AUTONOMO"
echo "  Backend:  http://localhost:8005"
echo "  Frontend: http://localhost:5173"
echo "============================================"

# Directorio raiz del modulo
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Matar procesos previos en esos puertos
echo "[1/3] Liberando puertos 8005 y 5173..."
fuser -k 8005/tcp 2>/dev/null || true
fuser -k 5173/tcp 2>/dev/null || true

# Arrancar Backend
echo "[2/3] Iniciando Backend (8005)..."
if [ -f "venv/bin/python" ]; then
    PYTHON="venv/bin/python"
else
    PYTHON="python3"
fi

$PYTHON -m uvicorn studio_api:app --host 0.0.0.0 --port 8005 --reload &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Esperar que backend arranque
sleep 3

# Arrancar Frontend
echo "[3/3] Iniciando Frontend (5173)..."
cd studio
npm run dev &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

echo ""
echo "============================================"
echo "  ✅ N04 Studio iniciado"
echo "  Abre: http://localhost:5173"
echo "  API:  http://localhost:8005/api/studio/ping"
echo "============================================"
echo ""
echo "Para detener: kill $BACKEND_PID $FRONTEND_PID"
echo "O usa: Ctrl+C"

# Esperar ambos procesos
wait $BACKEND_PID $FRONTEND_PID
