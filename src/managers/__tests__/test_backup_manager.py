from unittest import TestCase, main
from unittest.mock import Mock
import asyncio
from ..backup_manager import BackupManager


class TestBackupManager(TestCase):

    def setUp(self):
        self.backupper = BackupManager()

    def test__init__(self):
        with self.subTest('should load data if _LOAD_ON_INIT is True'):
            self.backupper._LOAD_ON_INIT = True
            self.backupper.load = Mock()

            self.backupper.__init__()

            self.assertTrue(self.backupper.load.called == 1)

    def test__del__(self):
        with self.subTest('should dump data if _DUMP_ON_DESTROY is True'):
            self.backupper._DUMP_ON_DESTROY = True
            self.backupper.dump = Mock()

            self.backupper.__del__()

            self.assertTrue(self.backupper.dump.called == 1)

    def test_load(self):
        with self.subTest('should set time of last load if load of data is successful'):
            self.backupper.__load__ = Mock(return_value=True)

            asyncio.run(self.backupper.load())

            self.assertTrue(self.backupper.__load__.called == 1)
            self.assertIsNotNone(self.backupper.last_load)

    def test_dump(self):
        with self.subTest('should set time of last dump if dump of data is successful'):
            self.backupper.__dump__ = Mock(return_value=True)

            asyncio.run(self.backupper.dump())

            self.assertTrue(self.backupper.__dump__.called == 1)
            self.assertIsNotNone(self.backupper.last_dump)

if __name__ == '__main__':
    main()
