class launcher:
    __is_enabled = False

    @property
    def is_enabled(self) -> bool:
        return self.__is_enabled

    @property
    def is_disabled(self) -> bool:
        return not self.__is_enabled

    def __del__(self) -> None:
        super().__del__()
        if self.__is_enabled:
            self.__disable__(self.__scope)

    def __enable__(self) -> None:
        """Is called to run execution."""
        pass

    def __disable__(self) -> None:
        """Is called to stop execution."""
        pass

    def enable(self) -> None:
        """Enable execution."""
        if self.is_disabled:
            self.__is_enabled = True
            self.__enable__()

    def disable(self) -> None:
        """Disable execution."""
        if self.is_enabled:
            self.__is_enabled = False
            self.__disable__()
