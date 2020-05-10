from typing import Union
from uuid import uuid4

class PointState:
    CONNECTED = 'CONNECTED'
    SEPARATED = 'SEPARATED'

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
        return bool(len(self.__connections))

    @property
    def is_separated(self) -> bool:
        return not self.is_connected()

    def __init__(self, name: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__name = name
        self.__uuid = uuid4()
        # TODO: connections {next, prev, all}
        self.__next = {} # TODO: если открою будет не безопасно
        self.__prev = {} # TODO: если открою будет не безопасно
        self.__connections = {} # TODO: если открою будет не безопасно
        self.__current_state = None

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
        return point in self.__connections

    def get_point(self, uuid: str) -> Union[Point, None]:
        """Return point if there is connection with point otherwise None."""
        if uuid in self.__connections:
            return self.__connections[uuid]

        return None

    def connect(self, point: Point) -> Point:
        """Add connection with point."""
        if not self.has_connection(point):
            self.__connections[point] = point
            self.__next[point] = point
            point.__prev[self] = self

            self.check_connections()
        return self

    def disconnect(self, point: Union[Point, str]) -> Point:
        """Disconnect from point."""
        if isinstance(point, str):
            point = self.get_point(point)

        if self.has_connection(point):
            del self.__connections[point]

            if point in self.__prev:
                del self.__prev[point]
                del point.__next[self]

            if point in self.__next:
                del self.__next[point]
                del point.__prev[self]

            self.check_connections()
        return self

    def separate(self) -> Point:
        """Disconnect from all connections."""
        for point in self.__connections.values():
            self.disconnect(point)

        return self

    def check_connections(self) -> None:
        """Check if point is connected to another point."""
        if self.is_connected and self.__current_state != PointState.CONNECTED:
            self.__connected__()
            self.__current_state = PointState.CONNECTED
        elif self.is_separated and self.__current_state != PointState.SEPARATED:
            self.__separated__()
            self.__current_state = PointState.SEPARATED

# TODO: point.look(data) -> boold типо если вернёт False мне точно туда ненадо?