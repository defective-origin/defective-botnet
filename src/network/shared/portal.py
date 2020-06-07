from typing import Union, Dict
from .launcher import Launcher
from socketio import AsyncClient, AsyncServer, WSGIApp
import eventlet

class Portal(Launcher):
    __portals = {}
    __server = None
    __host = 'localhost'
    __port = 5000


    def __commander__(self, connector: Union[AsyncClient, AsyncServer]) -> None:
        """Add handlers of the data emitted from portals."""
        pass

    def __enable__(self):
        sio = AsyncServer()
        app = WSGIApp(sio)
        address = (self.__host, self.__port)
        self.__server = eventlet.wsgi.server(eventlet.listen(address), app)

        sio.on('connect', func) # TODO: add socket to portals
        sio.on('disconnect', func) # TODO: remove socket from portals
        sio.on('message', func) # TODO: bind to commander without sid
        # TODO: sid
        # TODO: open server
        # TODO: reconnect socket server when it has error
        # TODO: connect with commander
        for url, portal in self.__portals.items():
            portal.connect(url)

    def __disable__(self):
        self.__server.stop()

        for portal in self.__portals.values():
            portal.disconnect()

    def open(self, url: str) -> Portal:
        """Create new portal."""
        if url not in self.__portals:
            client = AsyncClient()
            client.connect(url)
            self.__commander__(client)
            self.__portals[url] = client

    def close(self, url: str) -> Portal:
        """Close a portal."""
        if url in self.__portals:
            self.__portals[url].disconnect()
            del self.__portals[url]

    def emit(self, event: str, data: Union[str, bytes, dict, list]) -> Portal:
        """Emit data through all created portals."""
        for portal in self.__portals.values():
            portal.emit(event, data)
