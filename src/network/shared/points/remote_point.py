from .point import Point
from ..portal import Portal
import socketio

class RemotePoint(Point, Portal):
    """Connect to remote point."""
    @staticmethod
    def is_remote_point(point: Point) -> bool:
        return isinstance(point, RemotePoint)
    
    def __commander__(self, command: str, data: Any) -> None:
        pass

    def __emitter__(self) -> None: pass

    def send(self): pass

    def remote_connect(self): pass
    def remote_disconnect(self): pass

    def strengthen(self, point: Point, max_points: int) -> None: pass

    # TODO: connect to remote point by network(scoket)
    # TODO: disconnect from remote point by network
    # TODO: send command
    # TODO: reg command list
    # yа ините запустить сервер и пытаться постоянно подключаться при потере соединения
    # на деструкторе отключать сервер
    # TODO: объединить с точкой расширения?
