from typing import Dict, Callable
from .life_cycle import Launcher, WaterfallExecutor
from ..scope import Scope
import uuid

class Point(Launcher, WaterfallExecutor[Scope]):
    """
        Point of network. By default work as spread point.
    """

    @staticmethod
    def is_point(point: Point) -> bool:
        return type(point) == Point

    @property
    def name(self) -> str:
        return self.__name

    @property
    def uuid(self) -> str:
        return self.__uuid

    @property
    def is_separated(self) -> bool:
        connection_count = len(self.__prev) + len(self.__next)
        return not connection_count

    def __init__(self, name: str) -> None:
        self.__name = name
        self.__uuid = uuid.uuid4()
        self.__scope = None
        self.__next = {}
        self.__prev = {}

    def __str__(self) -> str:
        return f'{self.__name}({self.__uuid})' if self.__name else self.__uuid

    def __eq__(self, other) -> bool:
        if Point.is_point(self):
            return self.__uuid == other.__uuid
        elif isinstance(other, str):
            return self.__uuid == other
        return NotImplemented

    def __del__(self) -> None:
        if self.__is_enabled:
            self.__disable__(self.__scope)
    
    def __enable__(self, scope: Scope) -> None: # remove?
        """Is called to run point execution."""
        pass

    def __disable__(self, scope: Scope) -> None: # remove?
        """Is called to stop point execution."""
        pass
    # prev_scope curr_scope?
    def __scope__(self, scope: Scope) -> Scope:
        """Change scope for children points."""
        return scope
    
    # def __separated__(self, scope: Scope) -> None:
    #     """Is called when point has no connections."""
    #     pass
    # emit life-cycle point
    def __broadcaster__(self, scope: Scope, next_points: Dict[str,Point], prev_points: Dict[str,Point]) -> Callable:
        """Create next function built with execution children point."""
        def next(error: Exception = None):
            for point in next_points.values():
                point.exec(error)
        return next

    def has_connection(self, key: str) -> bool:
        """Return True if connected with point otherwise False."""
        return key in self.__next or key in self.__prev

    def get_point(self, key: str) -> Point:
        """Return point if there is connection with point otherwise None."""
        if key in self.__prev.keys():
            return self.__prev[key]

        if key in self.__next.keys():
            return self.__next[key]

        return None

    # def has_connection(self, point: Union[Point,str]) -> bool:
    #     """Return True if connected with point otherwise False."""
    #     uuid = point.uuid if Point.is_point(point) else point
    #     return uuid in self.__next or uuid in self.__prev

    def connect(self, point: Point) -> Point:
        """Add connection with point."""
        if not self.has_connection(point):
            self.__next[point.uuid] = point
            point.__prev[self.uuid] = self
        return self

    # TODO: work with name
    def disconnect(self, point: Point) -> Point:
        """Disconnect from point."""
        if self.has_connection(point):
            del self.__next[point.uuid]
            del point.__prev[self.uuid]

        # if self.is_separated:
        #     self.__separated__(self.__scope)

        return self

    def separate(self) -> Point:
        """Disconnect from all connections."""
        for prev_point in self.__prev.values():
            prev_point.disconnect(self)

        for next_point in self.__next.values():
            self.disconnect(next_point)

        # self.__separated__(self.__scope)

        return self

    def enable(self, scope: Scope, rebuild_scope: bool = False) -> Point: # rebuild scope is insecure
        """Build scope and enable point execution."""
        if not self.__scope or rebuild_scope:
            self.__scope = self.__scope__(scope)

        super().enable(self.__scope)

            # if self.is_separated:
            #     self.__separated__(self.__scope)

        return self

    def disable(self, scope: Scope) -> Point: # remove? add only for method interface
        """Disable point execution."""
        super().disable(self.__scope)
        return self

    # TODO: add call args and kwargs
    def exec(self, error: Exception = None) -> None:
        """Run point handlers and start a chain reaction of execution."""
        if self.is_disabled:
            return

        super().exec(error, self.__scope, self.__next, self.__prev)

# TODO: emit back to parent?
# TODO: if point is not connected with anything call __one__ by default destruct?
# if scope exist dont cill him? or let him get data from network scope himself