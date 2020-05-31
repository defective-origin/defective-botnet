from .point import Point

class PipePoint(Point): # TODO: network?
    """Связывает в жёсткий конвеер."""
    __pipe = []

    @staticmethod
    def is_pipe_point(point: Point) -> bool:
        return isinstance(point, PipePoint)

    def chain(self, *point: List[Point]) -> Point:
        if point in self.__pipe:
            return self

        if self.__pipe:
            self.__pipe[-1].connect(point)

        self.__pipe.extend(point)
        return self

    def unchain(self, point: Union[Point, str]) -> Point:
        if point in self.__pipe:
            index = self.__pipe.index(point)
            [prev, curr, next] = self.__pipe[prev: next + 1]

            if next:
                point.disconnect(next)
            
            if prev:
                point.disconnect(prev)
        self.__pipe.remove(point)
        return self

    # TODO: call pipe till exec


# TODO: send the scope to children
# TODO:
#prev points \._._._._._._./next points
#            /             \