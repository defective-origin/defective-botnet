from typing import Dict, Callable
from ..points.point import Point
from ..managers.launch_manager import LaunchManager
from ..managers.walk_manager import WalkManager
from ..scope import Scope

class Bot(Point, LaunchManager, WalkManager):
    """
        Point of network. By default work as spread point.
    """

    # prev_scope curr_scope?
    # def __scope__(self, scope: Scope) -> Scope:
    #     """Change scope for children points."""
    #     return scope

    # emit life-cycle point
    def __broadcaster__(self, scope: Scope, next_points: Dict[str,Point], prev_points: Dict[str,Point]) -> Callable:
        """Create next function built with execution children point."""
        def next(error: Exception = None):
            for point in next_points.values():
                point.exec(error)
        return next

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

    def look(self, data: Any) -> bool: pass
    
    
     # TODO: __look__ or __check__



# class WaterfallTrackwalker(Generic[EnvironmentType], Point, Trackwalker[EnvironmentType]):
#     def __tracker__(self, environment: EnvironmentType) -> Callable:
#         """Create next function built with execution next points."""
#         def next(error: Exception = None):
#             for point in self._next.values():
#                 point.exec(error, environment)
#         return next

# class BroadcastTrackwalker(Generic[EnvironmentType], Point, Trackwalker[EnvironmentType]):
#     def __tracker__(self, environment: EnvironmentType) -> Callable:
#         """Create next function built with execution next points."""
#         def next(error: Exception = None):
#             for point in self._connections.values():
#                 point.exec(error)
#         return next
