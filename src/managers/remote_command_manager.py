from typing import Union, Dict, Callable
from .launch_manager import LaunchManager
from multiprocessing import Process
from flask import Flask, request
import requests

class Events:
    REGISTER: 'REGISTER'
    UNREGISTER: 'UNREGISTER'

class RemoteCommandManager(LaunchManager):
    _portals = []
    __server = None
    __server_process = None

    # It must be redefined in the inherited class
    _CONNECT_PORTALS_ON_ENABLE = True
    _DISCONNECT_PORTALS_ON_DISABLE = True
    # It must be redefined in the inherited class in order to set the data for the server
    _HOST = 'localhost'
    _PORT = 5000

    @property
    def server_url(self) -> str:
        return f'https://{self._HOST}:{self._PORT}'

    def __commander__(self, register: Callable) -> None:
        """Add handlers of the data emitted from portals."""
        pass

    def __enable__(self) -> None:
        super().__enable__()

        self.__server = Flask()
        self.__register_handler(Events.REGISTER, lambda: self.register(request.get_json().url))
        self.__register_handler(Events.UNREGISTER, lambda: self.unregister(request.get_json().url))
        self.__commander__(self.__register_handler)

        kwargs = { 'host': self._HOST, 'port': self._PORT }
        self.__server_process = Process(target=self.__server.run, kwargs=kwargs)
        self.__server_process.start()

        if self._CONNECT_PORTALS_ON_ENABLE:
            json = { 'url': self.server_url }
            self.spread(Events.REGISTER, json)

    def __disable__(self) -> None:
        super().__disable__()

        if self._DISCONNECT_PORTALS_ON_DISABLE:
            json = { 'url': self.server_url }
            self.spread(Events.UNREGISTER, json)

        self.__server_process.terminate()
        self.__server_process.join()

    def register(self, url: str) -> None:
        """Register remote portal."""
        if url not in self._portals and self.server_url != url:
            self._portals.append(url)
            json = { 'url': self.server_url }
            self.send(url, Events.REGISTER, json)

    def unregister(self, url: str) -> None:
        """Unregister remote portal."""
        if url in self._portals:
            self._portals.remove(url)
            json = { 'url': self.server_url }
            self.send(url, Events.UNREGISTER, json)

    def spread(self, event: str, json: Union[str, bytes, dict, list] = {}, handler: Callable = None) -> None:
        """Send json data to all registered portals."""
        for portal in self._portals:
            self.send(portal, event, json, handler)

    def send(self, url: str, event: str, json: Union[str, bytes, dict, list] = {}, handler: Callable = None) -> None:
        """Send json data to one portal."""
        response = requests.post(f'{url}/{event}', json=json)
        if not handler:
            handler(response.json())

    def __register_handler(self, event: str, handler: Callable) -> None:
        """Add route handler to flask app."""
        self.__server.add_url_rule(f'/{event}', event, handler, methods=['POST'])
