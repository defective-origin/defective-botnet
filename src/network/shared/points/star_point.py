from .point import Point

class StarPoint(Point):
    """Подключается с 3 соседними элементами соседних точек для отказаустойчевости vожно указать сколько взять с каждого."""
    @staticmethod
    def is_star_point(point: Point) -> bool:
        return isinstance(point, StarPoint)

    # TODO: rewrite connect
    # TODO: rewrite dicconnect
    # TODO: also work with remote point
