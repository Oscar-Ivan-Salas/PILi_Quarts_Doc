"""
PILI WebSocket - Real-time Chat
Enterprise-grade WebSocket with connection management
Following python-patterns and clean-code skills
"""
from fastapi import WebSocket, WebSocketDisconnect, Depends
from typing import Dict, Set
import logging
import json
import asyncio
from uuid import UUID
from datetime import datetime

from ..core.brain import PILIBrain
from ..config.settings import get_settings
from .router import get_pili_brain

logger = logging.getLogger(__name__)
settings = get_settings()


class ConnectionManager:
    """
    WebSocket connection manager.
    
    Manages active connections, broadcasting, and heartbeat.
    Following clean-code: Single Responsibility
    """
    
    def __init__(self):
        # Active connections: {user_id: websocket}
        self.active_connections: Dict[str, WebSocket] = {}
        
        # Connection metadata
        self.connection_times: Dict[str, datetime] = {}
        
        # Heartbeat task
        self._heartbeat_task: asyncio.Task = None
        
        logger.info("Connection Manager initialized")
    
    async def connect(self, websocket: WebSocket, user_id: str):
        """
        Accept new WebSocket connection.
        
        Following python-patterns: Async for I/O
        """
        await websocket.accept()
        
        # Close existing connection if any
        if user_id in self.active_connections:
            await self.disconnect(user_id)
        
        self.active_connections[user_id] = websocket
        self.connection_times[user_id] = datetime.utcnow()
        
        logger.info(f"User {user_id} connected (total: {len(self.active_connections)})")
        
        # Start heartbeat if not running
        if self._heartbeat_task is None or self._heartbeat_task.done():
            self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
    
    async def disconnect(self, user_id: str):
        """Disconnect user"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].close()
            except Exception as e:
                logger.warning(f"Error closing connection for {user_id}: {e}")
            
            del self.active_connections[user_id]
            del self.connection_times[user_id]
            
            logger.info(f"User {user_id} disconnected (remaining: {len(self.active_connections)})")
    
    async def send_personal_message(self, message: dict, user_id: str):
        """
        Send message to specific user.
        
        Following clean-code: Clear method naming
        """
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except Exception as e:
                logger.error(f"Error sending message to {user_id}: {e}")
                await self.disconnect(user_id)
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connected users"""
        disconnected = []
        
        for user_id, websocket in self.active_connections.items():
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to {user_id}: {e}")
                disconnected.append(user_id)
        
        # Clean up disconnected users
        for user_id in disconnected:
            await self.disconnect(user_id)
    
    async def _heartbeat_loop(self):
        """
        Send periodic heartbeat to keep connections alive.
        
        Following python-patterns: Background task pattern
        """
        while self.active_connections:
            try:
                await asyncio.sleep(settings.ws_heartbeat_interval)
                
                # Send ping to all connections
                await self.broadcast({
                    "type": "heartbeat",
                    "timestamp": datetime.utcnow().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Heartbeat error: {e}", exc_info=True)
    
    def get_stats(self) -> dict:
        """Get connection statistics"""
        return {
            "active_connections": len(self.active_connections),
            "max_connections": settings.ws_max_connections,
            "users": list(self.active_connections.keys())
        }


# Global connection manager instance
manager = ConnectionManager()


async def websocket_endpoint(
    websocket: WebSocket,
    user_id: UUID,
    pili: PILIBrain = Depends(get_pili_brain)
):
    """
    WebSocket endpoint for real-time chat.
    
    Following api-patterns: WebSocket for real-time communication
    Following python-patterns: Async/await for I/O
    """
    user_id_str = str(user_id)
    
    # Check connection limit
    if len(manager.active_connections) >= settings.ws_max_connections:
        await websocket.close(code=1008, reason="Max connections reached")
        logger.warning(f"Connection rejected for {user_id_str}: max connections")
        return
    
    # Accept connection
    await manager.connect(websocket, user_id_str)
    
    try:
        # Send welcome message
        await manager.send_personal_message({
            "type": "connected",
            "message": "¡Hola! Soy PILI, tu asistente de ingeniería. ¿En qué puedo ayudarte?",
            "timestamp": datetime.utcnow().isoformat()
        }, user_id_str)
        
        # Message loop
        while True:
            # Receive message
            data = await websocket.receive_text()
            
            try:
                message_data = json.loads(data)
                message = message_data.get("message", "")
                context = message_data.get("context")
                
                if not message:
                    await manager.send_personal_message({
                        "type": "error",
                        "error": "Message cannot be empty",
                        "timestamp": datetime.utcnow().isoformat()
                    }, user_id_str)
                    continue
                
                # Send typing indicator
                await manager.send_personal_message({
                    "type": "typing",
                    "timestamp": datetime.utcnow().isoformat()
                }, user_id_str)
                
                # Process message with PILI
                result = await pili.process_message(
                    user_id=user_id_str,
                    message=message,
                    context=context
                )
                
                # Send response
                await manager.send_personal_message({
                    "type": "message",
                    "response": result["response"],
                    "extracted_data": result.get("extracted_data"),
                    "suggestions": result.get("suggestions", []),
                    "timestamp": result["timestamp"]
                }, user_id_str)
                
            except json.JSONDecodeError:
                await manager.send_personal_message({
                    "type": "error",
                    "error": "Invalid JSON format",
                    "timestamp": datetime.utcnow().isoformat()
                }, user_id_str)
            
            except Exception as e:
                logger.error(f"Error processing WebSocket message: {e}", exc_info=True)
                await manager.send_personal_message({
                    "type": "error",
                    "error": "Error processing message",
                    "message": str(e),
                    "timestamp": datetime.utcnow().isoformat()
                }, user_id_str)
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for user {user_id_str}")
        await manager.disconnect(user_id_str)
    
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id_str}: {e}", exc_info=True)
        await manager.disconnect(user_id_str)
