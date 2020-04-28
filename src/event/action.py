from typing import Callable

class Action:
    __NEUTRAL_STATE = 0
    def __init__(self, times: int, callback: Callable) -> None:
        self.__is_limited = isinstance(times, int) and times > self.__NEUTRAL_STATE
        self.__times = times if self.is_limited else self.__NEUTRAL_STATE
        self.__callback = callback

    def __eq__(self, other) -> bool:
        if callable(other):
            return self.__callback.__name__ == other.__name__
        return NotImplemented

    def is_limited(self) -> bool:
        """Return True if the action can be called only several times otherwise False."""
        return self.__is_limited

    def is_unlimited(self) -> bool:
        """Return True if the action can be called an unlimited number of times otherwise False."""
        return not self.__is_limited

    def is_usable(self) -> bool:
        """Return True if Action can be run otherwise False."""
        return self.is_unlimited() or self.__times > self.__NEUTRAL_STATE

    def exec(self, *args, **kwargs) -> None:
        """Call callback was given if the action is usable."""
        if self.is_usable():
            if self.is_limited():
                self.__times -= 1
            self.__callback(*args, **kwargs) # TODO: call asynchronously or through a promise

