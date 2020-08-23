from typing import TypeVar, Callable, Union
from .bot import Bot
from ..points.network_point import Network

StoreType = TypeVar('StoreType')

class Botnet(Bot, Network): # TODO: inherit from remotePoint?

    def __enable__(self) -> None:
        super().__enable__()
        for point in self._points.values():
            point.enable()

    def __disable__(self) -> None:
        super().__disable__()
        for point in self._points.values():
            point.disable()

    def __trackwalker__(self, received_store: StoreType) -> Callable:
        def next(error: Union[Exception, None] = None, store: Union[StoreType, None] = None):
            super().__trackwalker__()(error, store)
            self._core.exec(error, store)
        return next

    def build_store(self, store: StoreType, rebuild: bool = False) -> None: # TODO: call children building
        if not self._store or rebuild:
            self._store = self.__store__(store)

# TODO: если какой-то участок цепи падает, остальной должен регенерировать и не падать

 # TODO: fix documentation in all files