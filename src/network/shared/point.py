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
    def is_separated(self) -> bool:
        return not self.is_unseparated()

    @property
    def is_unseparated(self) -> bool:
        return bool(len(self.__connections))

    def __init__(self, name: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__name = name
        self.__uuid = uuid.uuid4()
        self.__next = {}
        self.__prev = {}
        self.__connections = {}

    def __str__(self) -> str:
        return f'{self.__name}({self.__uuid})' if self.__name else self.__uuid

    def __eq__(self, other) -> bool:
        if Point.is_point(self):
            return self.__uuid == other.__uuid
        elif isinstance(other, str):
            return self.__uuid == other
        return NotImplemented

    def __separated__(self) -> None:
        """Is called when point has no connections."""
        pass

    def __unseparated__(self) -> None:
        """Is called when point has connections."""
        pass

    def has_connection(self, key: str) -> bool:
        """Return True if connected with point otherwise False."""
        return key in self.__connections

    def get_point(self, key: str) -> Union[Point,None]:
        """Return point if there is connection with point otherwise None."""
        if key in self.__connections.keys():
            return self.__connections[key]

        return None

    def connect(self, point: Point) -> Point:
        """Add connection with point."""
        if not self.has_connection(point):
            self.__connections[point.uuid] = point
            self.__next[point.uuid] = point
            point.__prev[self.uuid] = self

        self.check_connections()
        return self

    # TODO: work with name
    def disconnect(self, point: Point) -> Point:
        """Disconnect from point."""
        if self.has_connection(point):
            del self.__connections[point.uuid]
            del self.__next[point.uuid]
            del point.__prev[self.uuid]

        self.check_connections()
        return self

    def separate(self) -> Point:
        """Disconnect from all connections."""
        for prev_point in self.__prev.values():
            prev_point.disconnect(self)

        for next_point in self.__next.values():
            self.disconnect(next_point)

        self.__connections = {}
        self.check_connections()

        return self

    def check_connections(self) -> None:
        """Check if point is connected to another point."""
        if self.is_separated: # TODO: run just one time
            self.__separated__()
        else:
            self.__unseparated__()



# TODO remove all Point types

class RemotePoint(Point):
    @staticmethod
    def is_remote_point(point: Point) -> bool:
        return isinstance(point, Point)

class ExpansionPoint(Point):
    @staticmethod
    def is_expansion_point(point: Point) -> bool:
        return isinstance(point, Point)

class NetworkPoint(Point):
    @staticmethod
    def is_network_point(point: Point) -> bool:
        return isinstance(point, Point)
