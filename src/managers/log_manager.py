from typing import Callable, List

class Environment:
    PRODUCTION = 'PRODUCTION'
    DEVELOPMENT = 'DEVELOPMENT'

class LogManager:
    def __init__(self, mode: Environment = Environment.DEVELOPMENT) -> None:
        self.__is_development_mode = mode == Environment.DEVELOPMENT

    def __log__(self, values: List) -> None: pass
    def __info__(self, values: List) -> None: pass
    def __warn__(self, values: List) -> None: pass
    def __error__(self, values: List) -> None: pass
    
    def log(self, *values: List) -> None:
        self.__handle_message(self.__log__, values)

    def info(self, *values: List) -> None:
        self.__handle_message(self.__info__, values)

    def warn(self, *values: List) -> None:
        self.__handle_message(self.__warn__, values)

    def error(self, *values: List) -> None:
        self.__handle_message(self.__error__, values)

    def __handle_message(self, handler: Callable, values: List):
        if self.__is_development_mode:
            print(*values)

        handler(values)