from typing import TypeVar, Generic, Callable, Union

EnvironmentType = TypeVar('EnvironmentType')

class WalkManager(Generic[EnvironmentType]):
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
        """
            Execute handlers.
            
            Tree traversal strategies:
            1) If the environment is transferred then it will be used it
            2) If the environment is built before execution then it will be used it
        """

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
