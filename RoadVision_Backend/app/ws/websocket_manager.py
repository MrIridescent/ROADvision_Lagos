# app/ws/websocket_manager.py

from fastapi import WebSocket
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Enhanced WebSocket manager for specific videos and Global Command Link"""
    
    def __init__(self):
        # Video-specific connections
        self.active_connections: Dict[str, WebSocket] = {}
        # Global command link connections
        self.command_link_connections: List[WebSocket] = []

    async def connect(self, video_id: str, websocket: WebSocket):
        """Accept and store WebSocket connection for a specific video"""
        await websocket.accept()
        self.active_connections[video_id] = websocket
        logger.info(f"WebSocket connected for video: {video_id}")

    def disconnect(self, video_id: str):
        """Remove specific video WebSocket connection"""
        if video_id in self.active_connections:
            del self.active_connections[video_id]
            logger.info(f"WebSocket disconnected for video: {video_id}")

    async def connect_command_link(self, websocket: WebSocket):
        """Connect to the global real-time communication channel"""
        await websocket.accept()
        self.command_link_connections.append(websocket)
        logger.info("New peer connected to Sentinel Command Link")

    def disconnect_command_link(self, websocket: WebSocket):
        """Disconnect from global channel"""
        if websocket in self.command_link_connections:
            self.command_link_connections.remove(websocket)
            logger.info("Peer disconnected from Command Link")

    async def send_message(self, video_id: str, message: dict):
        """Send message to specific video's WebSocket"""
        if video_id in self.active_connections:
            try:
                await self.active_connections[video_id].send_json(message)
            except Exception as e:
                logger.error(f"Error sending message to {video_id}: {str(e)}")
                self.disconnect(video_id)

    async def broadcast_command_link(self, message: dict):
        """Broadcast message to all command link participants"""
        for connection in self.command_link_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to command link: {e}")
                self.command_link_connections.remove(connection)

    async def broadcast(self, message: dict):
        """Legacy broadcast to all video-specific connections"""
        for video_id in list(self.active_connections.keys()):
            await self.send_message(video_id, message)

# Global manager instance
manager = ConnectionManager()
