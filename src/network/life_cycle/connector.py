class ConnectionPoint: # move to another folder?
    __next = {}
    __prev = {}

    @property
    def is_separated(self) -> bool:
        connection_count = len(self.__prev) + len(self.__next)
        return not connection_count

    def __separated__(self, scope: Scope) -> None:
        """Is called when point has no connections."""
        pass

    def has_connection(self, key: str) -> bool:
        """Return True if connected with point otherwise False."""
        return key in self.__next or key in self.__prev

    def get_point(self, key: str) -> Point:
        """Return point if there is connection with point otherwise None."""
        if key in self.__prev.keys():
            return self.__prev[key]

        if key in self.__next.keys():
            return self.__next[key]

        return None

    def connect(self, point: Point) -> None:
        """Add connection with point."""
        if not self.has_connection(point):
            self.__next[point.uuid] = point
            point.__prev[self.uuid] = self

    # TODO: work with name
    def disconnect(self, point: Point) -> None:
        """Disconnect from point."""
        if self.has_connection(point):
            # point = self.__next[point.uuid]
            del self.__next[point.uuid]
            del point.__prev[self.uuid]

        if self.is_separated:
            self.__separated__(self.__scope)

    def separate(self) -> None:
        """Disconnect from all connections."""
        for prev_point in self.__prev.values():
            prev_point.disconnect(self)

        for next_point in self.__next.values():
            self.disconnect(next_point)

        # self.__separated__(self.__scope)

# TODO remove all Point types

class RemoteConnectionPoint:
    pass
