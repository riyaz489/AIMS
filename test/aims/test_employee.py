import unittest
import mock
from aims.employee import Employee


class TestEmployee(unittest.TestCase):

    @mock.patch('aims.employee.ConnectDb')
    @mock.patch('aims.employee.Employee.file_complain', return_value='')
    @mock.patch('aims.employee.getattr')
    @mock.patch('builtins.input', return_value='')
    @mock.patch('aims.employee.os')
    @mock.patch('aims.employee.Menu')
    @mock.patch('builtins.print')
    def test_bdo_features(self, mock_print, mock_menu, mock_os, mock_input, mock_getattr, file_complain, mock_db):
        employee = Employee()
        mock_getattr.side_effect = [file_complain, SystemExit]
        self.assertRaises(SystemExit, employee.employee_features)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_getattr.call_count, 2)
        self.assertEqual(mock_input.call_count, 3)
        mock_os.system.assert_any_call('clear')
        self.assertEqual(mock_print.call_count, 6)

    @mock.patch('aims.employee.ConnectDb')
    @mock.patch('aims.employee.sys')
    @mock.patch('aims.employee.Menu', side_effect=Exception)
    @mock.patch('builtins.print')
    def test_bdo_features_exception(self, mock_print, mock_menu, mock_sys, mock_db):
        employee = Employee()
        employee.employee_features()
        mock_sys.exit.assert_called_once()
        self.assertEqual(mock_print.call_count, 4)

    @mock.patch('aims.employee.Menu')
    @mock.patch('aims.employee.ConnectDb')
    @mock.patch('builtins.input', return_value='')
    @mock.patch('builtins.print')
    def test_file_complain(self, mock_print, mock_input, mock_db, mock_menu):
        employee = Employee()
        employee.employee_id = 1
        mock_db().get_accident_types.return_value = [[1, 2]]
        mock_menu().draw_menu.return_value = 2
        employee.file_complain()
        mock_db().report_new_accident.assert_called_once()
        mock_db().commit_data.assert_called_once()

    @mock.patch('aims.employee.Menu')
    @mock.patch('aims.employee.ConnectDb')
    @mock.patch('builtins.input', return_value='')
    @mock.patch('builtins.print')
    def test_file_complain_exception(self, mock_print, mock_input, mock_db, mock_menu):
        employee = Employee()
        employee.employee_id = 1
        mock_db().get_accident_types.return_value = [[1, 2]]
        mock_menu().draw_menu.return_value = 2
        mock_db().commit_data.side_effect = Exception
        employee.file_complain()
        mock_db().report_new_accident.assert_called_once()
        self.assertEqual(3, mock_print.call_count)

    @mock.patch('aims.employee.Menu')
    @mock.patch('aims.employee.ConnectDb')
    @mock.patch('builtins.input', return_value='')
    @mock.patch('builtins.print')
    def test_file_complain_back_button(self, mock_print, mock_input, mock_db, mock_menu):
        employee = Employee()
        employee.employee_id = 1
        mock_db().get_accident_types.return_value = [[1, 2]]
        mock_menu().draw_menu.return_value = 'BACK'
        employee.file_complain()
        mock_db().get_accident_types.assert_called_once()
        mock_menu().draw_menu.asser_called_once()


if __name__ == '__main__':
    unittest.main()
