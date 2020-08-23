from typing import TypeVar, Generic, Callable, Union

StoreType = TypeVar('StoreType')

class WalkManager(Generic[StoreType]):
    _store = None

    def __store__(self, store: StoreType) -> StoreType:
        """Change store for children points."""
        return store

    def __trackwalker__(self, received_store: StoreType) -> Callable:
        """Create next function built with execution next points."""
        pass

    def __exec__(self, error: Exception, store: StoreType, next: Callable) -> None:
        """
            Is called when previous point don't raise error.
            By default call broadcast function.
        """
        next(error, store)

    def __catch__(self, error: Exception, store: StoreType, next: Callable) -> None:
        """
            Is called when previous point raise error.
            By default call broadcast function.
        """
        next(error, store)

    def __failed__(self, error: Exception, store: StoreType, next: Callable) -> None:
        """
            Is called when current point raise error.
            By default call broadcast function.
        """
        next(error, store)

    def __completed__(self, store: StoreType) -> None:
        """Is called when error is not raised in current execution."""
        pass

    def __finally__(self, store: StoreType) -> None:
        """Is called all time after point is handled."""
        pass

    def build_store(self, store: StoreType, rebuild: bool = False) -> None:
        """Build or rebuild store."""
        if not self._store or rebuild:
            self._store = self.__store__(store)

    async def exec(self, error: Union[Exception, None] = None, store: Union[StoreType, None] = None) -> None:
        """
            Run point handlers and start a chain reaction of execution.
            
            Tree traversal strategies:
            1) If the store is transferred then it will be used it
            2) If the store is built before execution then it will be used it
        """

        next = self.__trackwalker__(store)
        store = self.__store__(store) if store else self._store
        try:
            if error:
                self.__catch__(error, store, next)
            else:
                self.__exec__(error, store, next)
        except Exception as catched_error:
            self.__failed__(catched_error, store, next)
        else:
            self.__completed__(store)
        finally:
            self.__finally__(store)
