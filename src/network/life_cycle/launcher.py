class launcher:
    __is_enabled = False

    @property
    def is_enabled(self) -> bool:
        return self.__is_enabled

    @property
    def is_disabled(self) -> bool:
        return not self.__is_enabled

    def __enable__(self, *args, **kwargs) -> None:
        """Is called to run execution."""
        pass

    def __disable__(self, *args, **kwargs) -> None:
        """Is called to stop execution."""
        pass

    def enable(self, *args, **kwargs) -> None:
        """Enable execution."""
        if self.is_disabled:
            self.__is_enabled = True
            self.__enable__(*args, **kwargs)

    def disable(self, *args, **kwargs) -> None:
        """Disable execution."""
        if self.is_enabled:
            self.__is_enabled = False
            self.__disable__(*args, **kwargs)
