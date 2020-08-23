from typing import Union
from uuid import uuid4

class PointState:
    CONNECTED = 'CONNECTED'
    SEPARATED = 'SEPARATED'

class Connections:
    prev = {}
    next = {}
    all = {}

class Point:
    """Point of network."""

    @staticmethod
    def is_point(point: Point) -> bool:
        return isinstance(point, Point)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def uuid(self) -> str:
        return self.__uuid

    @property
    def is_connected(self) -> bool:
        return bool(len(self._connections.all))

    @property
    def is_separated(self) -> bool:
        return not self.is_connected()

    def __init__(self, name: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__name = name
        self.__uuid = uuid4()
        self.__current_state = None
        self._connections = Connections()

    def __str__(self) -> str:
        return f'{self.__name}({self.__uuid})' if self.__name else self.__uuid

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other) -> bool:
        if Point.is_point(self):
            return self.__uuid == other.__uuid
        elif isinstance(other, str):
            return self.__uuid == other
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.__uuid)

    def __separated__(self) -> None:
        """Is called when point has no connections."""
        pass

    def __connected__(self) -> None:
        """Is called when point has connections."""
        pass

    def has_connection(self, point: Union[Point, str]) -> bool:
        """Return True if connected with point otherwise False."""
        return point in self._connections.all

    def get_point(self, uuid: str) -> Union[Point, None]:
        """Return point if there is connection with point otherwise None."""
        return self._connections.all.get(uuid, None)

    def connect(self, point: Point, max_points: int = 0) -> None:
        """Connection with point."""
        if not self.has_connection(point):
            self._connections.all[point] = point
            self._connections.next[point] = point
            point._connections.prev[self] = self

            self.strengthen(point, max_points)
            self.check_connections()

    def disconnect(self, point: Point) -> None:
        """Disconnect from point."""

        if self.has_connection(point):
            del self._connections.all[point]

            if point in self._connections.prev:
                del self._connections.prev[point]
                del point._connections.next[self]

            if point in self._connections.next:
                del self._connections.next[point]
                del point._connections.prev[self]

            self.check_connections()

    def separate(self) -> None:
        """Disconnect from all connections."""
        for point in self._connections.all.values():
            self.disconnect(point)

    def check_connections(self) -> None:
        """Check if point is connected to another point."""
        if self.is_connected and self.__current_state != PointState.CONNECTED:
            self.__connected__()
            self.__current_state = PointState.CONNECTED
        elif self.is_separated and self.__current_state != PointState.SEPARATED:
            self.__separated__()
            self.__current_state = PointState.SEPARATED

    def strengthen(self, point: Point, max_points: int = 0) -> None:
        """Add next points from given point to current point. By default all next points of given point."""
        next_connection = point._connections.next.values()
        max_points = max_points if max_points else len(next_connection)
        for point in next_connection[:max_points]:
            self.connect(point)
