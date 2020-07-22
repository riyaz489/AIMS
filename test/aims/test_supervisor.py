import unittest
import mock
from aims.supervisor import Supervisor


class TestSupervisor(unittest.TestCase):

    @mock.patch('aims.supervisor.Supervisor.show_accident_complain', return_value='')
    @mock.patch('aims.supervisor.getattr')
    @mock.patch('builtins.input', return_value='')
    @mock.patch('aims.supervisor.os')
    @mock.patch('aims.supervisor.Menu')
    @mock.patch('builtins.print')
    def test_bdo_features(self, mock_print, mock_menu, mock_os, mock_input, mock_getattr, show_accidents):
        supervisor = Supervisor()
        mock_getattr.side_effect = [show_accidents, SystemExit]
        self.assertRaises(SystemExit, supervisor.supervisor_features)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_getattr.call_count, 2)
        self.assertEqual(mock_input.call_count, 3)
        mock_os.system.assert_any_call('clear')
        mock_print.assert_any_call("choose feature :\n")

    @mock.patch('aims.supervisor.sys')
    @mock.patch('aims.supervisor.Menu', side_effect=Exception)
    @mock.patch('builtins.print')
    def test_bdo_features_exception(self, mock_print, mock_menu, mock_sys):
        supervisor = Supervisor()
        supervisor.supervisor_features()
        mock_sys.exit.assert_called_once()
        self.assertEqual(mock_print.call_count, 2)

    @mock.patch('builtins.input', return_value='')
    @mock.patch('builtins.print')
    @mock.patch('aims.supervisor.Admin')
    @mock.patch('aims.supervisor.ConnectDb')
    def test_show_accident_complain(self, mock_db, mock_admin, mock_print, mock_input):
        supervisor = Supervisor()
        supervisor.supervisor_id = 1
        mock_admin.choose_multiple_employee.return_value = [1, 2]
        supervisor.show_accident_complain()
        mock_db.commit_data.called_once()
        mock_db.register_supervisor_report.called_once()
        self.assertEqual(mock_print.call_count, 5)

    @mock.patch('builtins.input', return_value='')
    @mock.patch('builtins.print')
    @mock.patch('aims.supervisor.Admin')
    @mock.patch('aims.supervisor.ConnectDb')
    def test_show_accident_complain_exception(self, mock_db, mock_admin, mock_print, mock_input):
        supervisor = Supervisor()
        supervisor.supervisor_id = 1
        mock_db().register_supervisor_report.side_effect = Exception
        mock_admin.choose_multiple_employee.return_value = [1, 2]
        supervisor.show_accident_complain()
        mock_db.rollback_data.called_once()
        self.assertEqual(mock_print.call_count, 6)

    @mock.patch('builtins.input', return_value='')
    @mock.patch('builtins.print')
    @mock.patch('aims.supervisor.Admin')
    @mock.patch('aims.supervisor.ConnectDb')
    def test_show_accident_complain_no_accident(self, mock_db, mock_admin, mock_print, mock_input):
        supervisor = Supervisor()
        supervisor.supervisor_id = 1
        mock_admin().show_table_menu.return_value = None
        supervisor.show_accident_complain()
        mock_db.show_supervisor_accidents.called_once()
        self.assertEqual(mock_print.call_count, 1)


if __name__ == '__main__':
    unittest.main()
