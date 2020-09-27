from unittest import TestCase, main
from unittest.mock import Mock
import asyncio
from ..action import Action


class TestAction(TestCase):
    def test__eq__(self):
        with self.subTest('should compare callbacks by name'):
            mock_callback = lambda: None
            action = Action(0, mock_callback)

            self.assertTrue(action.__eq__(mock_callback))

    def test_is_usable(self):
        with self.subTest('should return true if action is unlimited'):
            mock_callback = lambda: None
            action = Action(None, mock_callback)

            self.assertTrue(action.is_usable)
        
        with self.subTest('should return true if action has count of execution'):
            mock_callback = lambda: None
            action = Action(1, mock_callback)

            self.assertTrue(action.is_usable)

    def test_exec(self):
        with self.subTest('should call callback if action is usable'):
            mock_callback = Mock()
            action = Action(1, mock_callback)

            asyncio.run(action.exec())

            self.assertTrue(mock_callback.is_called)
        
        with self.subTest('should not call callback if action is not usable'):
            mock_callback = Mock()
            action = Action(0, mock_callback)

            asyncio.run(action.exec())

            self.assertTrue(mock_callback.is_not_called)

        with self.subTest('should become unusable if allowed count of execution is 0'):
            mock_callback = Mock()
            action = Action(1, mock_callback)

            asyncio.run(action.exec())

            self.assertFalse(action.is_usable)

if __name__ == '__main__':
    main()
