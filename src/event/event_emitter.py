from typing import Callable, Union
from .event import Event
from .base_event import BaseEvent
import re

# TODO: set via decorator?
class EventEmitter(BaseEvent):
    __events = {}

    def __parse_names(self, names: str) -> List[str]:
        """Return all names in string."""
        return re.sub(' +', ' ', names.strip()).split()

    def on(self, names: str, callback: Callable) -> EventEmitter:
        """Add unlimited action to event."""
        return self.once(names, None, callback)

    def once(self, names: str, times: int, callback: Callable) -> EventEmitter:
        """Add limited action to event."""
        for name in self.__parse_names(names):
            if not self.contains(name):
                self.__events[name] = Event()
            self.__events[name].once(times, callback)
        return self

    def off(self, names: str, callback: Union[Callable,None] = None) -> EventEmitter:
        """Remove event by the name or remove only action from event if the callback was given."""
        for name in self.__parse_names(names):
            if not self.contains(name):
                return
            
            if callback:
                self.__events[name].off(callback)
            else:
                del self.__events[name]
        return self

    def enable(self, names: str) -> EventEmitter:
        """Enable the event by the name. After that it can be emitted."""
        for name in self.__parse_names(names):
            if self.contains(name):
                self.__events[name].enable()
        return self

    def disable(self, names: str) -> EventEmitter:
        """Disable the event by the name. After that it can't be emitted."""
        for name in self.__parse_names(names):
            if self.contains(name):
                self.__events[name].disable()
        return self

    def is_enabled(self, name: str) -> Union[bool,None]:
        """
            Return True if the event with given name is enabled otherwise False.
            If name is not found it returns None.
        """
        return self.__events[name].is_enabled() if self.contains(name) else None

    def is_disabled(self, name: str) -> Union[bool,None]:
        """
            Return True if the event with given name is disabled otherwise False.
            If name is not found it returns None.
        """
        return self.__events[name].is_disabled() if self.contains(name) else None

    async def emit(self, names: str, *args, **kwargs) -> None:
        """Emit events by names."""
        for name in self.__parse_names(names):
            if name in self.__events:
                self.__events[name].emit(*args, **kwargs)
