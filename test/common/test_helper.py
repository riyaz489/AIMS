import unittest
import mock
from pynput.keyboard import Key
from common.helper import *

class MockValidation:

    def __init__(self):
        self.n = self.mock_validation()

    def mock_validation(self, *args):
        yield False
        yield True

    def mock_next(self, *args):
        t2 = next(self.n)
        return t2


class HelperTest(unittest.TestCase):

    @mock.patch('builtins.print')
    @mock.patch('common.helper.PrettyTable')
    def test_raw_data_to_table(self, mock_table, mock_print):
        raw_data = [[1, 2], [3, 4]]
        cols = ['a', 'b']
        raw_data_to_table(cols, raw_data)
        self.assertEqual(mock_table().add_row.call_count, 2)
        mock_print.assert_called_once()

    def test_always_true(self):
        self.assertEqual(always_true(), True)

    def test_on_press_up(self):
        mock_press_key = mock.Mock()
        mock_press_key.name = 'up'
        menu = Menu()
        menu.count = 3
        menu.on_press(mock_press_key)
        self.assertEqual(menu.index, 3)
        menu.on_press(mock_press_key)
        self.assertEqual(menu.index, 2)

    def test_on_press_down(self):
        mock_press_key = mock.Mock()
        mock_press_key.name = 'down'
        menu = Menu()
        menu.count = 3
        menu.index = 3
        self.assertEqual(menu.on_press(mock_press_key), False)
        self.assertEqual(menu.index, 0)
        menu.on_press(mock_press_key)
        self.assertEqual(menu.index, 1)

    @mock.patch('common.helper.Key')
    def test_on_press_enter(self, mock_key):
        mock_press_key = mock_key.enter
        menu = Menu()
        menu.count = 3
        self.assertEqual(menu.on_press(mock_press_key), False)
        self.assertEqual(menu.flag, 1)

    @mock.patch('common.helper.Key')
    def test_on_press_exception(self, mock_key):
        mock_press_key = Exception
        menu = Menu()
        self.assertEqual(menu.on_press(mock_press_key), False)

    @mock.patch('common.helper.Listener')
    def test_draw_menu(self, mock_listener):
        menu = Menu()
        items = ['first', 'second', 'EXIT']
        menu.index = 1
        menu.flag = 1
        result = menu.draw_menu(items)
        self.assertEqual(result, items[1])

    @mock.patch('builtins.print')
    @mock.patch('common.helper.Listener')
    def test_draw_menu_exit(self, mock_listener, mock_print):
        menu = Menu()
        items = ['first', 'second', 'EXIT']
        menu.index = 2
        menu.flag = 1
        self.assertRaises(SystemExit, menu.draw_menu, items)
        mock_print.assert_called_once_with('exiting from system')

    @mock.patch('common.helper.always_true')
    @mock.patch('common.helper.os')
    @mock.patch('builtins.print')
    @mock.patch('common.helper.Listener')
    def test_draw_menu_print(self, mock_listener, mock_print, mock_os, mock_always_true):
        mock_always_true.return_value = False
        menu = Menu()
        items = ['first', 'second', 'EXIT']
        menu.index = 1
        menu.flag = 0
        menu.draw_menu(items)

        self.assertEqual(mock_print.call_count, 3)
        mock_listener.assert_called_once()
        mock_os.system.assert_called_once_with('clear')

    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    def test_input_validation(self, mock_print, mock_input):
        v = MockValidation()
        mock_input.return_value = 'dummy'
        result = input_validation('dummy', v.mock_next, 'dummy')
        self.assertEqual(mock_print.call_count, 1)
        self.assertEqual(mock_input.call_count, 2)
        self.assertEqual(result, 'dummy')


if __name__ == '__main__':
    unittest.main()
