from typing import TypeVar, Generic, Callable, Union

EnvironmentType = TypeVar('EnvironmentType')

class Trackwalker(Generic[EnvironmentType]):
    """
        # TODO: DOC this strategies
        стратегии обхода
        1) передавать стор чтобы в 1 стор писался весь отчет
        2) строить каждомуц свой стор чтобы они в общий сбрасывали
        3) одиночное выполнение
    """
    _environment = None

    def __environment__(self, environment: EnvironmentType) -> EnvironmentType:
        """Change environment for children points."""
        return environment

    def __trackfinder__(self, environment: EnvironmentType) -> Callable:
        """Create next function built with execution next points."""
        pass

    def __exec__(self, error: Exception, environment: EnvironmentType, next: Callable) -> None:
        """
            Is called when previous point don't raise error.
            By default call broadcast function.
        """
        next()

    def __catch__(self, error: Exception, environment: EnvironmentType, next: Callable) -> None:
        """
            Is called when previous point raise error.
            By default call broadcast function.
        """
        next()

    def __failed__(self, error: Exception, environment: EnvironmentType, next: Callable) -> None:
        """
            Is called when current point raise error.
            By default call broadcast function.
        """
        next()

    def __completed__(self, environment: EnvironmentType) -> None:
        """Is called when error is not raised in current execution."""
        pass

    def __finally__(self, environment: EnvironmentType) -> None:
        """Is called all time after point is handled."""
        pass

    def build_environment(self, environment: EnvironmentType, rebuild: bool = False):
        """Build or rebuild environment."""
        if not self._environment or rebuild:
            self.__environment__(environment)

    async def exec(self, error: Union[Exception, None] = None, environment: Union[EnvironmentType, None] = None) -> None:
        """Execute handlers."""

        if environment:
            environment = self.__environment__(environment)
        else:
            environment = self._environment

        next = self.__trackfinder__(environment)
        try:
            if error:
                self.__catch__(error, environment, next)
            else:
                self.__exec__(error, environment, next)
        except Exception as catched_error:
            self.__failed__(catched_error, environment, next)
        else:
            self.__completed__(environment)
        finally:
            self.__finally__(environment)

# class WaterfallTrackwalker(Generic[EnvironmentType], Point, Trackwalker[EnvironmentType]):
#     def __tracker__(self, environment: EnvironmentType) -> Callable:
#         """Create next function built with execution next points."""
#         def next(error: Exception = None):
#             for point in self._next.values():
#                 point.exec(error, environment)
#         return next

# class BroadcastTrackwalker(Generic[EnvironmentType], Point, Trackwalker[EnvironmentType]):
#     def __tracker__(self, environment: EnvironmentType) -> Callable:
#         """Create next function built with execution next points."""
#         def next(error: Exception = None):
#             for point in self._connections.values():
#                 point.exec(error)
#         return next
