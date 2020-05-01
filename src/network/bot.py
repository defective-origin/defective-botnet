from typing import Dict, Callable
from .shared.point import Point
from .shared.launcher import Launcher
from .shared.executor import WaterfallExecutor
from ..scope import Scope
import uuid

class Bot(Point, Launcher, WaterfallExecutor[Scope]):
    """
        Point of network. By default work as spread point.
    """

    def __del__(self) -> None:
        if self.__is_enabled:
            self.__disable__(self.__scope)
    
    # def __enable__(self, scope: Scope) -> None: # remove?
    #     """Is called to run point execution."""
    #     pass

    # def __disable__(self, scope: Scope) -> None: # remove?
    #     """Is called to stop point execution."""
    #     pass
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
            self.__scope = self.__scope__(scope) # TODO: move to waterfall

        super().enable(self.__scope)

        return self

    def disable(self, scope: Scope) -> Point: # remove? add only for method interface
        """Disable point execution."""
        super().disable(self.__scope)
        return self

    def exec(self, error: Exception = None) -> None:
        """Run point handlers and start a chain reaction of execution."""
        if self.is_disabled:
            return

        super().exec(error, self.__scope, self.__next, self.__prev)

# TODO: emit back to parent?
# TODO: if point is not connected with anything call __one__ by default destruct?
# if scope exist dont cill him? or let him get data from network scope himself