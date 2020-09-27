from unittest import TestCase, main
from unittest.mock import Mock
import asyncio
from ..walk_manager import WalkManager


class TestWalkManager(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.walker = WalkManager()

    def test_build_store(self):
        test_store = { 'STORE': 'ORIGIN' }

        with self.subTest('should set store if store is not set'):
            self.walker.build_store(test_store)

            self.assertDictEqual(self.walker._store, test_store, 'store is not set')

        with self.subTest('should rebuild store if store is set and rebuild flag is True'):
            self.walker.build_store(test_store, True)

            new_store = { 'STORE': 'NEW' }
            self.walker.build_store(new_store, True)

            self.assertDictEqual(self.walker._store, new_store, 'store is not rebuild')

        with self.subTest('should not rebuild store if store is set and rebuild flag is False'):
            self.walker.build_store(test_store, True)
            
            new_store = { 'STORE': 'NEW' }
            self.walker.build_store(new_store, False)

            self.assertDictEqual(self.walker._store, test_store, 'store is rebuild')

    def test_exec(self):
        test_store = { 'STORE': 'ORIGIN' }

        with self.subTest('should call __catch__ if error is transferred'):
            self.walker.__catch__ = Mock()

            asyncio.run(self.walker.exec(Exception('TEST'), test_store))

            self.assertTrue(self.walker.__catch__.is_called)

        with self.subTest('should call __exec__ if error is not transferred'):
            self.walker.__exec__ = Mock()

            asyncio.run(self.walker.exec(store=test_store))

            self.assertTrue(self.walker.__exec__.is_called)

        with self.subTest('should call __failed__ if error is risen during execution of __catch__'):
            self.walker.__failed__ = Mock()
            self.walker.__catch__ = Mock(side_effect=Exception('TEST'))

            asyncio.run(self.walker.exec(store=test_store))

            self.assertTrue(self.walker.__failed__.is_called)

        with self.subTest('should call __failed__ if error is risen during execution of __exec__'):
            self.walker.__failed__ = Mock()
            self.walker.__exec__ = Mock(side_effect=Exception('TEST'))

            asyncio.run(self.walker.exec(store=test_store))

            self.assertTrue(self.walker.__failed__.is_not_called)

        with self.subTest('should call __completed__ if __catch__ or __exec__ executed without error'):
            self.walker.__completed__ = Mock()

            asyncio.run(self.walker.exec(store=test_store))

            self.assertTrue(self.walker.__completed__.is_called)

        with self.subTest('should not call __completed__ if __catch__ executed with error'):
            self.walker.__completed__ = Mock()
            self.walker.__catch__ = Mock(side_effect=Exception('TEST'))

            asyncio.run(self.walker.exec(store=test_store))

            self.assertTrue(self.walker.__completed__.is_not_called)

        with self.subTest('should not call __completed__ if __exec__ executed with error'):
            self.walker.__completed__ = Mock()
            self.walker.__exec__ = Mock(side_effect=Exception('TEST'))

            asyncio.run(self.walker.exec(store=test_store))

            self.assertTrue(self.walker.__completed__.is_not_called)

        with self.subTest('should call __finally__ after all operations if error is risen or not'):
            self.walker.__finally__ = Mock()

            asyncio.run(self.walker.exec(store=test_store))

            self.assertTrue(self.walker.__finally__.is_called)

        with self.subTest('should call __finally__ even if __catch__ raises error'):
            self.walker.__completed__ = Mock()
            self.walker.__catch__ = Mock(side_effect=Exception('TEST'))

            asyncio.run(self.walker.exec(store=test_store))

            self.assertTrue(self.walker.__finally__.is_called)

        with self.subTest('should call __finally__ even if __exec__ raises error'):
            self.walker.__completed__ = Mock()
            self.walker.__exec__ = Mock(side_effect=Exception('TEST'))

            asyncio.run(self.walker.exec(store=test_store))

            self.assertTrue(self.walker.__finally__.is_called)

    def test__select_store(self):
        test_store = { 'STORE': 'ORIGIN' }

        with self.subTest('should return own store if the store is not transferred'):
            self.walker.build_store(test_store)
            result = self.walker._WalkManager__select_store()

            self.assertDictEqual(result, test_store, 'store is not equal')

        with self.subTest('should return transferred store if the store is transferred'):
            self.walker.build_store(test_store)

            new_store = { 'STORE': 'NEW' }
            result = self.walker._WalkManager__select_store(new_store)

            self.assertDictEqual(result, new_store, 'store is not equal')


if __name__ == '__main__':
    main()
