from unittest import TestCase, main
from unittest.mock import Mock
from ..backup_manager import BackupManager


class TestBackupManager(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.backupper = BackupManager()

    def test__init__(self):
        with self.subTest('should load data if _LOAD_ON_INIT is True'):
            self.backupper._LOAD_ON_INIT = True
            self.backupper.load = Mock()

            self.backupper.__init__()

            self.assertTrue(self.backupper.load.is_called)

    def test__del__(self):
        with self.subTest('should dump data if _DUMP_ON_DESTROY is True'):
            self.backupper._DUMP_ON_DESTROY = True
            self.backupper.dump = Mock()

            self.backupper.__del__()

            self.assertTrue(self.backupper.dump.is_called)

    def test_load(self):
        with self.subTest('should set time of last load if load of data is successful'):
            self.backupper.__load__ = Mock(return_value=True)

            self.backupper.load()

            self.assertTrue(self.backupper.__load__.is_called)
            self.assertIsNotNone(self.backupper.last_load)

    def test_dump(self):
        with self.subTest('should set time of last dump if dump of data is successful'):
            self.backupper.__dump__ = Mock(return_value=True)

            self.backupper.dump()

            self.assertTrue(self.backupper.__dump__.is_called)
            self.assertIsNotNone(self.backupper.last_dump)

if __name__ == '__main__':
    main()
