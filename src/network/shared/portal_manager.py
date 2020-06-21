from typing import Union, Dict, Callable
from .launcher import Launcher
from socketio import AsyncClient
from multiprocessing import Process
from flask import Flask, request
from flask_socketio import SocketIO, emit

import eventlet

# TODO: or change socket to http?
class PortalManager(Launcher):
    __sockets = {}
    __server = None

    # It must be redefined in the inherited class in order to set the data for the server
    _HOST = 'localhost'
    _PORT = 5000

    def __commander__(self, register: Callable) -> None:
        """Add handlers of the data emitted from portals."""
        pass

    def __enable__(self):
        super().__enable__()

        app = Flask()
        socketio = SocketIO(app)
        socketio.on_event('connect', lambda: self.__add_socket(request.remote_addr, request.namespace.socket))
        socketio.on_event('disconnect', lambda: self.close(request.remote_addr))
        self.__commander__(socketio.on_event)

        kwargs = { 'host': self._HOST, 'port': self._PORT }
        self.__server = Process(target=socketio.run, args=[app], kwargs=kwargs)
        self.__server.start()

        for url, portal in self.__sockets.items():
            portal.connect(url)

    def __disable__(self):
        super().__disable__()

        self.__server.terminate()
        self.__server.join()
        
        for portal in self.__sockets.values():
            portal.disconnect()

    def open(self, url: str) -> PortalManager:
        """Create new portal."""
        if url not in self.__sockets:
            client = AsyncClient()
            self.__commander__(client.on)
            self.__sockets[url] = client
            client.connect(url)

    def close(self, url: str) -> PortalManager:
        """Close a portal."""
        if url in self.__sockets:
            self.__sockets[url].disconnect()
            del self.__sockets[url]

    # TODO: add method only for one url
    def emit(self, event: str, data: Union[str, bytes, dict, list]) -> PortalManager:
        """Emit data through all created portals."""
        for portal in self.__sockets.values():
            portal.emit(event, data)

    def __add_socket(self, url: str, socket: AsyncClient) -> None:
        """Add socket by url."""
        self.__sockets[request.remote_addr] = socket
