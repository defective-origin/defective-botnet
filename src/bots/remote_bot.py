from typing import TypeVar, Callable, Union
from .bot import Bot
from ..points.remote_point import RemotePoint

StoreType = TypeVar('StoreType')

class RemoteBot(Bot, RemotePoint):

    def __trackwalker__(self, received_store: StoreType) -> Callable:
        def next(error: Union[Exception, None] = None, store: Union[StoreType, None] = None):
            super().__trackwalker__()(error, store)
            self._core.exec(error, store)
        return next

    def exec(self, error: Union[Exception, None] = None, store: Union[StoreType, None] = None) -> None: # TODO: call remote exec
        if self.is_enabled:
            super().exec(error, store)
