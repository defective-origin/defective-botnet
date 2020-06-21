from .point import Point
from ..portal_manager import PortalManager
import socketio

class RemotePoint(Point, PortalManager):
    """Connect to remote point."""
    @staticmethod
    def is_remote_point(point: Point) -> bool:
        return isinstance(point, RemotePoint)

    def __commander__(self, register: Callable) -> None:
        """Add handlers of the data emitted from portals."""
        register('get connections', lambda: super().emit('strengthen', { 'urls': self.__sockets.keys() })) # TODO: set url
        register('strengthen', lambda urls: map(lambda url: super().open(url), urls)) # TODO

    def connect(self, point: [Point, str], max_points: int = 0) -> RemotePoint:
        """Connection with local or remote point."""
        if isinstance(point, str):
            self.open(point)
            self.strengthen(point, max_points) # TODO: he can be no connected yet
        else:
            super().connect(point, max_points)
            super().strengthen(point, max_points)

    def disconnect(self, point: [Point, str]) -> RemotePoint:
        """Disconnect from local or remote point."""
        if isinstance(point, str):
            self.close(point)
        else:
            super().disconnect(point)

    def strengthen(self, point: [Point, str], max_points: int = 0) -> RemotePoint:
        """
            If given an url then connect to remote poits
            that is connected with repote point otherwise
            Add next points from given point to current point.
            By default all next points of given point.
        """
        if isinstance(point, str):
            self.emit('get connections', { 'max_points': max_points })
        else:
            super().strengthen(point, max_points)
    
    # yа ините запустить сервер и пытаться постоянно подключаться при потере соединения
    # на деструкторе отключать сервер
    # TODO: объединить с точкой расширения?
