from unittest import TestCase, main
from unittest.mock import Mock
from ..remote_command_manager import RemoteCommandManager


class TestRemoteCommandManager(TestCase):

    def setUp(self):
        self.remote_command_manager = RemoteCommandManager()

    def test_server_url(self):
        with self.subTest('should return url'):
            self.remote_command_manager._HOST = 'TEST_HOST'
            self.remote_command_manager._PORT = 'TEST_PORT'

            self.assertEqual(self.remote_command_manager.server_url, 'https://TEST_HOST:TEST_PORT')

    def test_spread(self):
        with self.subTest('should send data to all portals'):
            self.remote_command_manager._portals = ['PORTAL 1', 'PORTAL 2']
            self.remote_command_manager.send = Mock()

            self.remote_command_manager.spread('TEST EVENT')

            self.assertTrue(self.remote_command_manager.send.called == 2)

if __name__ == '__main__':
    main()
