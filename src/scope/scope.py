from .object import Object
from .constants import Operation
from ..event.event_emitter import EventEmitter

class Scope(Object, EventEmmiter):
    def __setitem__(self, attr: str, value: Any) -> None:
        self.__setattr__(attr, value)

    def __delitem__(self, attr: str) -> None:
        self.__delattr__(attr)

    def __setattr__(self, attr: str, value: Any) -> None:
        self.emit(attr, self[attr], value, Operation.SET)
        super().__setattr__(attr, value)

    def __delattr__(self, attr: str) -> None:
        self.emit(attr, self[attr], None, Operation.DELETE)
        super().__delattr__(attr)
# TODO add subscription