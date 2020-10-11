from unittest import TestCase, main
from unittest.mock import Mock
from ..launch_manager import LaunchManager


class TestLaunchManager(TestCase):

    def setUp(self):
        self.launcher = LaunchManager()

    def test__init__(self):
        with self.subTest('should enable if _ENABLE_ON_INIT is True'):
            self.launcher._ENABLE_ON_INIT = True
            self.launcher.enable = Mock()

            self.launcher.__init__()

            self.assertTrue(self.launcher.enable.is_called)

    def test__del__(self):
        with self.subTest('should disable if _DISABLE_ON_DESTROY is True'):
            self.launcher._DISABLE_ON_DESTROY = True
            self.launcher.disable = Mock()

            self.launcher.__del__()

            self.assertTrue(self.launcher.disable.is_called)

    def test_enable(self):
        with self.subTest('should enable if it is disabled'):
            self.launcher._LaunchManager__is_enabled = False
            self.launcher.__enable__ = Mock()

            self.launcher.enable()

            self.assertTrue(self.launcher.__enable__.called == 1)

        with self.subTest('should change state'):
            self.launcher._LaunchManager__is_enabled = False

            self.launcher.enable()

            self.assertTrue(self.launcher.is_enabled)

    def test_disable(self):
        with self.subTest('should disable if it is enabled'):
            self.launcher._LaunchManager__is_enabled = True
            self.launcher.__disable__ = Mock()

            self.launcher.disable()

            self.assertTrue(self.launcher.__disable__.called == 1)

        with self.subTest('should change state'):
            self.launcher._LaunchManager__is_enabled = True

            self.launcher.disable()

            self.assertTrue(self.launcher.is_disabled)

    def test_restart(self):
        with self.subTest('should restart'):
            self.launcher.disable = Mock()
            self.launcher.enable = Mock()

            self.launcher.restart()

            self.assertTrue(self.launcher.disable.called == 1)
            self.assertTrue(self.launcher.enable.called == 1)

if __name__ == '__main__':
    main()
