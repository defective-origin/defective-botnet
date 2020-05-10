from .point import Point

class ExpansionPoint(Point):
    """Downloaad files with points and connect this points with current point."""
    @staticmethod
    def is_expansion_point(point: Point) -> bool:
        return isinstance(point, ExpansionPoint)

    
    # TODO: install points via package manager and connect to this point
    # TODO: download points from internet(file, http, socket) and connect to this point
    # TODO: init and connect point from file(that was saved via downloading)
