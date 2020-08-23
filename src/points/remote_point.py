from flask import jsonify, request
from .point import Point
from ..managers.remote_command_manager import RemoteCommandManager

class Events:
    CONNECTIONS: 'CONNECTIONS'

class RemotePoint(Point, RemoteCommandManager):
    """Connect to remote point."""

    def __commander__(self, register: Callable) -> None:
        """Add handlers of the data emitted from portals."""
        register(Events.CONNECTIONS, self.__on_connections)

    def __on_connections(self) -> Any:
        max_points = request.get_json().max_points
        connections = self._portals[:max_points]
        return jsonify({ 'connections': connections })

    def connect(self, point: [Point, str], max_points: int = 0) -> None:
        """Connection with local or remote point."""
        if isinstance(point, str):
            self.register(point)
            self.strengthen(point, max_points)
        else:
            super().connect(point, max_points)

    def disconnect(self, point: [Point, str]) -> None:
        """Disconnect from local or remote point."""
        if isinstance(point, str):
            self.unregister(point)
        else:
            super().disconnect(point)

    def strengthen(self, point: [Point, str], max_points: int = 0) -> None:
        """Strengthen local or remote point."""
        if isinstance(point, str):
            if max_points > 0:
                json = { 'max_points': max_points }
                self.send(point, Events.CONNECTIONS, json, self.__strengthen_remote_point)
        else:
            super().strengthen(point, max_points)

    def __strengthen_remote_point(self, json: Any) -> None:
        for url in json.connections:
            self.register(url)
