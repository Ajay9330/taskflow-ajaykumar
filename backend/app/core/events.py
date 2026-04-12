import asyncio
import json
from typing import Dict, Set, Any
from uuid import UUID

class ConnectionManager:
    def __init__(self):
        # Maps project_id (str) to a set of queues
        self.active_connections: Dict[str, Set[asyncio.Queue]] = {}

    async def subscribe(self, project_id: UUID) -> asyncio.Queue:
        project_str = str(project_id)
        queue = asyncio.Queue()
        if project_str not in self.active_connections:
            self.active_connections[project_str] = set()
        self.active_connections[project_str].add(queue)
        return queue

    async def unsubscribe(self, project_id: UUID, queue: asyncio.Queue):
        project_str = str(project_id)
        if project_str in self.active_connections:
            self.active_connections[project_str].discard(queue)
            if not self.active_connections[project_str]:
                del self.active_connections[project_str]

    async def broadcast(self, project_id: UUID, message: Any):
        project_str = str(project_id)
        if project_str in self.active_connections:
            # Prepare message string once
            event_data = {
                "project_id": project_str,
                "payload": message
            }
            # Iterate over a copy of the set to avoid issues if set changes during iteration
            for queue in self.active_connections[project_str].copy():
                await queue.put(event_data)

manager = ConnectionManager()
