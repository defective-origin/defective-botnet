from .point import Point
from ..scope import Scope
# TODO: fix documentation in all files
class Builder(Point):
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
        # self.__enabled = []
        # self.__disabled = []

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
        self.__add_subnetworks(points)
        connection_point = self.__get_connection_point()
        for point in points:
            connection_point.connect(point)
            connection_point = point

        self.__current_pipe = connection_point

        return self

    def branch(self, *points: List[Point]) -> Network:
        """Branch points from the current point."""
        self.__add_subnetworks(points)
        connection_point = self.__get_connection_point()
        self.connection_point.branch(*points)
        self.__current_pipe = None

        return self

    def enable(self, scope: Scope = Scope()) -> None:
        """Run subnetworks and and all children points."""
        super().enable(scope)
        self.__core.enable(scope)

    def disable(self, scope: Scope) -> None: # disable children?
        """Stop subnetworks and all children points."""
        super().disable(scope)
        self.__core.disable(scope)

    # TODO: должен запустить только себя?
    def enable(self, scope: Scope, chain_reaction: bool = False) -> Point:
        """Build scope and enable network execution."""
        if not self.__is_enabled:
            self.__is_enabled = True
            self.__scope = self.__scope__(scope)
            self.__enable__(self.__scope)

        if chain_reaction: # incorrect
            for next_point in self.__next:
                next_point.enable(self.__scope, chain_reaction) # какой скоуп надо передавать?
        return self

    # TODO: должен остановить только себя?
    # TODO: впаду в рекурсию
    def disable(self, scope: Scope, chain_reaction: bool = False) -> Point:
        """Disable network execution."""
        if self.__is_enabled:
            self.__is_enabled = False
            self.__disable__(scope)

        # TODO: move to network?
        if chain_reaction: # incorrect
            for next_point in self.__next:
                next_point.disable(scope, chain_reaction)
        return self
        
        # TODO: unconnect self from all?

    def __add_subnetworks(self, *points: List[Point]) -> None:
        network_points = filter(Network.is_network, points)
        super().connect(network_points)

    def __get_connection_point(self) -> Point:
        return self.__current_pipe if self.__current_pipe else self.__current_node

# TODO: if network has name add as other network
# TODO: if node has name add to main nodes

# TODO: add subnetworks to next

# TODO: handle if inner network or outer one
# TODO: change scope and add name


# network turn off all points
# point turn off self

# TODO: если несколько разных точек свфяязанно с другой сетью и я говорю останоиться как быть? родителей считать? и они же другую сеть остановят
# TODO: если какой-то участок цепи падает, остальной должен регенерировать и не падать
# при добавление родителя в некст добавлять?
# TODO: add pipe?
 # TODO: Handle if the point is from other network or was executed alredy

 # if network then emit otherwise None