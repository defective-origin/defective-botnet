from typing import TypeVar, Callable, Union
from ..points.point import Point
from ..managers.launch_manager import LaunchManager
from ..managers.walk_manager import WalkManager

StoreType = TypeVar('StoreType')

class Bot(Generic[StoreType], Point, LaunchManager, WalkManager): # TODO: add other managers
    """Bot of botnet. By default work as spread point."""

    def __trackwalker__(self, received_store: StoreType) -> Callable:
        """Create next function built with execution next points."""
        def next(error: Union[Exception, None] = None, store: Union[StoreType, None] = None):
            store = store if store else received_store
            for point in self._connections.next.values():
                point.exec(error, store)
        return next

    def exec(self, error: Union[Exception, None] = None, store: Union[StoreType, None] = None) -> None:
        if self.is_enabled:
            super().exec(error, store)
