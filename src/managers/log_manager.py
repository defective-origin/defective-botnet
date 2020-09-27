class LogManager:
    def __log__(self, *args, **kwargs) -> None: pass
    def __info__(self, *args, **kwargs) -> None: pass
    def __warn__(self, *args, **kwargs) -> None: pass
    def __error__(self, *args, **kwargs) -> None: pass
    
    def log(self, *args, **kwargs) -> None:
        self.__log__(*args, **kwargs)

    def info(self, *args, **kwargs) -> None:
        self.__info__(*args, **kwargs)

    def warn(self, *args, **kwargs) -> None:
        self.__warn__(*args, **kwargs)

    def error(self, *args, **kwargs) -> None:
        self.__error__(*args, **kwargs)
