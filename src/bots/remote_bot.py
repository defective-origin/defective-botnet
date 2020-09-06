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

    def exec(self, error: Union[Exception, None] = None, store: Union[StoreType, None] = None) -> None:
        if self.is_enabled:
            self.spread(Events.EXEC) # TODO: send changed data
            super().exec(error, store)
