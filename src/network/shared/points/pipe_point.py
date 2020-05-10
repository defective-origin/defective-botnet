from .point import Point

class PipePoint(Point):
    """Связывает в жёсткий конвеер."""
    __pipe = []

    @staticmethod
    def is_pipe_point(point: Point) -> bool:
        return isinstance(point, PipePoint)

    def chain(self, *point: List[Point]) -> Point: # TODO: change name?
        self.__pipe.extend(point)
        return self

    def unchain(self, point: Union[Point, str]) -> Point: # TODO: change name?
        self.__pipe = filter(lambda p: p != point ,self.__pipe)
        return self

    # TODO: call pipe till exec
