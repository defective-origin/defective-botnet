from typing import Dict, TypeVar, Generic, Callable

Space = TypeVar('Space')

class WaterfallExecutor(Generic[Space]):
    __scope = None # TODO: add scope

    def __broadcaster__(self, space: Space, *args, **kwargs) -> Callable:
        """Create next function built with execution children point."""
        pass

    def __handler__(self, error: Exception, space: Space, next: Callable) -> None:
        """
            Is called when previous point don't raise error.
            By default call broadcast function.
        """
        next()

    def __error__(self, error: Exception, space: Space, next: Callable) -> None:
        """
            Is called when previous point raise error.
            By default call broadcast function.
        """
        next()

    def __failed__(self, error: Exception, space: Space, next: Callable) -> None:
        """
            Is called when current point raise error.
            By default call broadcast function.
        """
        next()

    def __completed__(self, space: Space) -> None:
        """Is called when error is not raised in current execution."""
        pass

    def __finally__(self, space: Space) -> None:
        """Is called all time after point is handled."""
        pass

    async def exec(self, error: Exception, space: Space, *args, **kwargs) -> None: # TODO: remove args kwargs
        """Execute handlers."""

        next = self.__broadcaster__(space, *args, **kwargs)
        try:
            if error:
                self.__error__(error, space, next)
            else:
                self.__handler__(error, space, next)
        except Exception as catched_error:
            self.__failed__(catched_error, space, next)
        else:
            self.__completed__(space)
        finally:
            self.__finally__(space)
