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

    def set_current_node(self, point: Point) -> Network:
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

    def unbrunch(self): pass # TODO:
# get point?
# TODO: add builder functions
