from typing import TypeVar, Callable, Union
from .bot import Bot
from ..points.remote_point import RemotePoint

StoreType = TypeVar('StoreType')

class Events:
    EXEC: 'EXEC'

class RemoteBot(Bot, RemotePoint):

    def __commander__(self, register: Callable) -> None:
        super().__commander__(register)
        register(Events.EXEC, super().exec)

    def __trackwalker__(self, received_store: StoreType) -> Callable:
        def next(error: Union[Exception, None] = None, store: Union[StoreType, None] = None):
            super().__trackwalker__()(error, store)
            self.spread(Events.EXEC)
        return next
