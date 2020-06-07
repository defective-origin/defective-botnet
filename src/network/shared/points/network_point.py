from .point import Point

class NetworkPoint(Point):
    """Combine points to one network point."""
    @staticmethod
    def is_network_point(point: Point) -> bool:
        return isinstance(point, NetworkPoint)

    def __init__(self, *args, core: Point = Point(), name: str = '', **kwargs) -> None:
        super().__init__(name, *args, **kwargs)
        self.__core = core
        self.__current_node = core
        self.__current_pipe = None
        self.__points = {}

    def set_current_point(self, point: Point) -> Network:
        """Set point as current to connect other points."""
        self.__current_pipe = None
        self.__current_node = point
        return self

    def chain(self, *points: List[Point]) -> Network:
        """Chain points and add to the current point."""
        connection_point = self.__get_connection_point()
        for point in points:
            connection_point.connect(point)
            connection_point = point
            self.__points[point.uuid] = point

        self.__current_pipe = connection_point

        return self

    def branch(self, *points: List[Point]) -> Network:
        """Branch points from the current point."""
        connection_point = self.__get_connection_point()
        for point in points:
            self.connection_point.connect(point)
            self.__points[point.uuid] = point

        self.__current_pipe = None

        return self

    def __get_connection_point(self) -> Point:
        return self.__current_pipe if self.__current_pipe else self.__current_node

    def unbrunch(self, uuid: Union[Point, str]) -> Point:
        """Separate point from all connections. Connect all previous points with next points."""
        point = Point if Point.is_point(Point) else self.__points[point.uuid]

        for prev_point in point._connections.prev:
            for next_point in point._connections.next:
                prev_point.connect(next_point)
        
        point.separate()
        return self

    def swap(self, point1: Point, point2: Point) -> Point:
        """Swap points."""
        [point1._connections, point2._connections] = [point2._connections, point1._connections]
        return self

    def get_network_point(self, uuid: str) -> Union[Point, None]:
        """Return point if there is point in network otherwise None."""
        if uuid in self.__points:
            return self.__points[uuid]

        return None

# TODO: connect via decorator? @connect(name)     combine(builder1, builder2 ...)