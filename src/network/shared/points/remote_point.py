from .point import Point
from ..portal import Portal
import socketio

class RemotePoint(Point, Portal):
    """Connect to remote point."""
    @staticmethod
    def is_remote_point(point: Point) -> bool:
        return isinstance(point, RemotePoint)

    def remote_connect(self): pass
    def remote_disconnect(self): pass

    def strengthen(self, point: Point, max_points: int) -> None: pass 

    # TODO: create virtual point for remote points

    # TODO: connect to remote point by network(scoket)
    # TODO: disconnect from remote point by network
    # yа ините запустить сервер и пытаться постоянно подключаться при потере соединения
    # на деструкторе отключать сервер
    # TODO: объединить с точкой расширения?
