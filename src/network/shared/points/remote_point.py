from .point import Point

class RemotePoint(Point):
    """Connect to remote point."""
    @staticmethod
    def is_remote_point(point: Point) -> bool:
        return isinstance(point, RemotePoint)
    
    # TODO: connect to remote point by network(scoket)
    # TODO: disconnect from remote point by network
    # TODO: send command
    # TODO: reg command list
