from .point import Point
from ..scope import Scope
# TODO: fix documentation in all files
class Network(Point):
    """
        Network builder.
    """

    @staticmethod
    def is_network(point: Point) -> bool:
        return type(point) == Network

    def __init__(self, core: Point = Point(), name: str = '') -> None:
        super().__init__(name)
        self.__core = core
        self.__current_node = core
        self.__current_pipe = None
        self.__points = {}

    def __broadcaster__(self, scope: Scope) -> Callable:
        def next(error: Exception = None):
            self.__core.exec(error)
        return next

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

    def enable(self, scope: Scope) -> Network:
        """Enable network and all children points."""
        super().enable(scope)

        for point in self.__points.values():
            point.enable(self.__scope) # control scope which given to the children
        return self

    def disable(self, scope: Scope) -> Network:
        """Disable network and all children points."""
        super().disable(scope)

        for point in self.__points.values():
            point.disable(self.__scope)
        return self

    def __get_connection_point(self) -> Point:
        return self.__current_pipe if self.__current_pipe else self.__current_node


# TODO: если несколько разных точек свфяязанно с другой сетью и я говорю останоиться как быть? родителей считать? и они же другую сеть остановят
# TODO: если какой-то участок цепи падает, остальной должен регенерировать и не падать

# TODO: add pipe?

 # if network then emit otherwise None

 # point1.move(point1, save_releshionship?)
 # add builder functions
 # TODO: add library 'templates'