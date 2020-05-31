import importlib
from .point import Point
import subprocess
import sys
import wget

class ExpansionPoint(Point):
    """Downloaad files with points and connect this points with current point."""
    @staticmethod
    def is_expansion_point(point: Point) -> bool:
        return isinstance(point, ExpansionPoint)
    
     # TODO: points via package manager and connect to this point
    def install(self, package_name: str) -> Point: # TODO: bad idia
        """Install point from python package manager."""
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        importlib.import_module(package_name)

    def download(self, url: str, path: str, protocol: str) -> Point:
        """Download point as file."""
        wget.download(url, path)
        # TODO: wget or curl
        # TODO: points from internet(file, ftps, https, socket, github) and connect to this point
        # TODO: secure (login pass, ...)

    def expand(self, file_path: str) -> Point:
        """Load point from file and connect with current point."""
    # TODO: init and connect point from file(that was saved via downloading)

# TODO: dynamic load structure from backup
# TODO: dynamic expand network
# restore from backup
# name / id  |  file_path | class_name
# name / id  |     url    | auth settings
# file_path | class_name
#    url    | auth settings
# TODO: save log after apdate data
