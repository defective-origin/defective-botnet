from typing import TypeVar, Callable, Union
from .bot import Bot
from ..points.network_point import NetworkPoint

StoreType = TypeVar('StoreType')

class Botnet(Bot, NetworkPoint):

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

    def build_store(self, store: StoreType, rebuild: bool = False) -> None:
        super().build_store(store, rebuild)
        for point in self._points.values():
            point.build_store(self._store, rebuild)

# TODO: if any point of chain breaks another must regenerate the chain

 # TODO: fix documentation in all files