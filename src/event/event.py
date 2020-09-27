from __future__ import annotations
from typing import Callable, List, Union
from .base_event import BaseEvent
from .action import Action

class Event(BaseEvent):
    __actions = {}
    __is_enabled = True

    def on(self, callback: Callable) -> Event:
        """Add unlimited action."""
        return self.once(None, callback)

    def once(self, times: Union[int, None], callback: Callable) -> Event:
        """Add limited action."""
        action = Action(times, callback)
        self.__actions[callback] = action
        return self

    def off(self, callback: Callable) -> Event:
        """Remove actions by callback name."""
        if callback in self.__actions:
            del self.__actions[callback]
        return self

    def enable(self) -> Event:
        """Enable the event. After that it can be emitted."""
        self.__is_enabled = True
        return self

    def disable(self) -> Event:
        """Disable the event. After that it can't be emitted."""
        self.__is_enabled = False
        return self

    def is_enabled(self) -> bool:
        """Return True if the event is enabled otherwise False."""
        return self.__is_enabled

    def is_disabled(self) -> bool:
        """Return True if the event is disabled otherwise False."""
        return not self.__is_enabled

    async def emit(self, *args, **kwargs) -> None:
        """
            Execute all actions in the event if the event is not disabled
            and remove all unusable actions.
        """
        if self.is_disabled(): return

        left_actions = {}
        for key, action in self.__actions.items():
            action.exec(*args, **kwargs)
            if action.is_usable():
                left_actions[key] = action
        self.__actions = left_actions
