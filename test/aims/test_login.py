import unittest
import mock
from aims.login import main


class LoginTest(unittest.TestCase):

    @mock.patch('aims.login.Employee')
    @mock.patch('aims.login.decrypt_pass', return_value='pass')
    @mock.patch('aims.login.ConnectDb')
    @mock.patch('builtins.input', return_value='sample')
    @mock.patch('aims.login.getpass', return_value='pass')
    @mock.patch('aims.login.Menu')
    @mock.patch('aims.login.os')
    def test_main_employee(self, mock_os, mock_menu, mock_pass, mock_input, mock_db, mock_decrypt, mock_employee):
        mock_db().get_user_info.return_value = ['1', 'pass']
        mock_menu().draw_menu.return_value = 'EMPLOYEE'
        main()
        mock_decrypt.assert_called_once()
        mock_employee.assert_called_once()
        mock_db().close_conn.assert_called_once()
        mock_employee().employee_features.assert_called_once()
        mock_pass.assert_called_once()
        self.assertEqual(mock_os.system.call_count, 2)
        self.assertEqual(mock_input.call_count, 2)

    @mock.patch('aims.login.Supervisor')
    @mock.patch('aims.login.decrypt_pass', return_value='pass')
    @mock.patch('aims.login.ConnectDb')
    @mock.patch('aims.login.input', return_value='sample')
    @mock.patch('aims.login.getpass', return_value='pass')
    @mock.patch('aims.login.Menu')
    @mock.patch('aims.login.os')
    def test_main_supervisor(self, mock_os, mock_menu, mock_pass, mock_input, mock_db,
                      mock_decrypt, mock_supervisor):
        mock_db().get_user_info.return_value = ['2', 'pass']
        mock_db().get_user_role.return_value = 'dummy'
        mock_menu().draw_menu.return_value = 'SUPERVISOR'
        main()
        mock_supervisor.assert_called_once()
        mock_decrypt.assert_called_once()
        mock_pass.assert_called_once()
        mock_db().close_conn.assert_called_once()
        mock_supervisor().supervisor_features.assert_called_once()
        self.assertEqual(mock_supervisor().supervisor_id, '2')
        self.assertEqual(mock_os.system.call_count, 2)
        self.assertEqual(mock_input.call_count, 2)

    @mock.patch('aims.login.Admin')
    @mock.patch('aims.login.decrypt_pass', return_value='pass')
    @mock.patch('aims.login.ConnectDb')
    @mock.patch('aims.login.input', return_value='sample')
    @mock.patch('aims.login.getpass', return_value='pass')
    @mock.patch('aims.login.Menu')
    @mock.patch('aims.login.os')
    def test_main_admin(self, mock_os, mock_menu, mock_pass, mock_input, mock_db, mock_decrypt, mock_admin):
        mock_db().get_user_info.return_value = ['3', 'pass']
        mock_db().get_user_role.return_value = 'dummy'
        mock_menu().draw_menu.return_value = 'ADMIN'
        main()
        mock_admin.assert_called_once()
        mock_db().close_conn.assert_called_once()
        mock_pass.assert_called_once()
        mock_decrypt.assert_called_once()
        mock_admin().admin_features.assert_called_once()
        self.assertEqual(mock_admin().admin_id, '3')
        self.assertEqual(mock_os.system.call_count, 2)
        self.assertEqual(mock_input.call_count, 2)

    @mock.patch('aims.login.decrypt_pass', return_value='pass2')
    @mock.patch('aims.login.ConnectDb')
    @mock.patch('builtins.input', return_value='sample')
    @mock.patch('aims.login.getpass', return_value='pass')
    @mock.patch('aims.login.Menu')
    @mock.patch('aims.login.os')
    @mock.patch('builtins.print')
    def test_main_invalid_credentials(self, mock_print, mock_os, mock_menu, mock_pass, mock_input, mock_db, mock_decrypt):
        mock_db().get_user_info.return_value = ['1', 'pass2']
        mock_menu().draw_menu.return_value = 'EMPLOYEE'
        mock_os.system.side_effect = ['', '', SystemExit]
        self.assertRaises(SystemExit, main)
        mock_decrypt.assert_called_once()
        mock_pass.assert_called_once()
        self.assertEqual(mock_os.system.call_count, 3)
        self.assertEqual(mock_input.call_count, 3)

    @mock.patch('aims.login.decrypt_pass', return_value='pass')
    @mock.patch('aims.login.ConnectDb')
    @mock.patch('builtins.input', return_value='sample')
    @mock.patch('aims.login.getpass', return_value='pass')
    @mock.patch('aims.login.Menu')
    @mock.patch('aims.login.os')
    @mock.patch('builtins.print')
    def test_main_not_authorized(self, mock_print, mock_os, mock_menu, mock_pass, mock_input, mock_db, mock_decrypt):
        mock_db().get_user_info.return_value = ['3', 'pass']
        mock_db().get_user_role.return_value = None
        mock_menu().draw_menu.return_value = 'ADMIN'
        mock_os.system.side_effect = ['', '', SystemExit]
        self.assertRaises(SystemExit, main)
        mock_decrypt.assert_called_once()
        mock_pass.assert_called_once()
        self.assertEqual(mock_os.system.call_count, 3)
        self.assertEqual(mock_input.call_count, 3)

    @mock.patch('builtins.print')
    @mock.patch('aims.login.sys')
    @mock.patch('aims.login.ConnectDb')
    @mock.patch('aims.login.os')
    def test_main_exception(self, mock_os, mock_db, mock_sys, mock_print):
        mock_os.system.side_effect = Exception
        main()

        mock_sys.exit.assert_called_once()
        mock_print.assert_called_once()
        mock_db().close_conn.assert_called_once()


if __name__ == '__main__':
    unittest.main()
