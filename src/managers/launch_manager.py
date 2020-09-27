class LaunchManager:
    __is_enabled = False

    # It must be redefined in the inherited class
    _ENABLE_ON_INIT = False
    _DISABLE_ON_DESTROY = True

    @property
    def is_enabled(self) -> bool:
        return self.__is_enabled

    @property
    def is_disabled(self) -> bool:
        return not self.__is_enabled

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if self._ENABLE_ON_INIT:
            self.enable()

    def __del__(self) -> None:
        if self._DISABLE_ON_DESTROY:
            self.disable()

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

    def restart(self) -> None:
        """Restart execution."""
        self.disable()
        self.enable()
