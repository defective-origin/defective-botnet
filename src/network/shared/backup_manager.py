from datetime import datetime

class BackupManager:
    """Serves to save and load the state of the object."""

    @property
    def last_load(self) -> datetime:
        return self.__last_load

    @property
    def last_dump(self) -> datetime:
        return self.__last_dump

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__last_load = None
        self.__last_dump = None

        self.load()

    def __del__(self) -> None:
        super().__del__()
        self.__dump__(self.__last_dump)

    def __load__(self, last_call: datetime) -> bool:
        """Load data from any resource. Return True if loading is success otherwise False."""

    def __dump__(self, last_call: datetime) -> bool:
        """Dump data to any resource. Return True if dumping is success otherwise False."""

    async def load(self) -> None:
        """Load data from any resource."""
        if self.__load__(self.__last_load):
            self.__last_load = datetime.now()

    async def dump(self) -> None:
        """Dump data to any resource."""
        if self.__dump__(self.__last_dump):
            self.__last_dump = datetime.now()
