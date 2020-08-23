from .point import Point

class NetworkPoint(Point):
    """Combine points to one network point."""

    def __init__(self, *args, core: Point = Point(), name: str = '', **kwargs) -> None:
        super().__init__(name, *args, **kwargs)
        self.__current_node = core
        self.__current_pipe = None
        self._core = core
        self._points = {}

    def set_current_point(self, point: Point) -> None:
        """Set point as current to connect other points."""
        self.__current_pipe = None
        self.__current_node = point

    def chain(self, *points: List[Point]) -> None:
        """Chain points and add to the current point."""
        connection_point = self.__get_connection_point()
        for point in points:
            connection_point.connect(point)
            connection_point = point
            self._points[point.uuid] = point

        self.__current_pipe = connection_point

    def branch(self, *points: List[Point]) -> None:
        """Branch points from the current point."""
        connection_point = self.__get_connection_point()
        for point in points:
            self.connection_point.connect(point)
            self._points[point.uuid] = point

        self.__current_pipe = None

    def __get_connection_point(self) -> Point:
        return self.__current_pipe if self.__current_pipe else self.__current_node

    def unbrunch(self, uuid: Union[Point, str]) -> None:
        """Separate point from all connections. Connect all previous points with next points."""
        point = Point if Point.is_point(Point) else self._points[point.uuid]

        for prev_point in point._connections.prev:
            for next_point in point._connections.next:
                prev_point.connect(next_point)
        
        point.separate()

    def swap(self, point1: Point, point2: Point) -> None:
        """Swap points."""
        [point1._connections, point2._connections] = [point2._connections, point1._connections]

    def get_network_point(self, uuid: str) -> Union[Point, None]:
        """Return point if there is point in network otherwise None."""
        if uuid in self._points:
            return self._points[uuid]

        return None
