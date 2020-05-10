from .point import Point

class BackupPoint(Point): # TODO: is not point TODO: save as json? при этом сохраняет связи для сбора с бэкапа сети
    """Сохраняет свое состояние куда-нибудь."""
    @staticmethod
    def is_backup_point(point: Point) -> bool:
        return isinstance(point, StarPoint)

    # TODO: dump (json or other type)
    # TODO: load (json or other type)
    # TODO: dump load to remote server
