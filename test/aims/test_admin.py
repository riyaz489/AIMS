import sqlite3
import unittest
import mock
from aims.admin import Admin


class MockCursor:
    def __init__(self, *args):
        self.description = [[1], [2], [3]]

    def fetchall(self, *args):
        return [[1], [2]]
    
    
class TestAdmin(unittest.TestCase):

    @mock.patch('aims.admin.Admin.accident_complains', return_value='')
    @mock.patch('aims.admin.getattr')
    @mock.patch('builtins.input', return_value='')
    @mock.patch('aims.admin.os')
    @mock.patch('aims.admin.Menu')
    @mock.patch('builtins.print')
    def test_admin_features(self, mock_print, mock_menu, mock_os, mock_input, mock_getattr, accident_complains):
        admin = Admin()
        mock_getattr.side_effect = [accident_complains, SystemExit]
        self.assertRaises(SystemExit, admin.admin_features)
        self.assertEqual(mock_menu().draw_menu.call_count, 2)
        self.assertEqual(mock_getattr.call_count, 2)
        self.assertEqual(mock_input.call_count, 3)
        mock_os.system.assert_any_call('clear')
        mock_print.assert_any_call("choose feature :\n")

    @mock.patch('aims.admin.sys')
    @mock.patch('aims.admin.Menu', side_effect=Exception)
    @mock.patch('builtins.print')
    def test_admin_features_exception(self, mock_print, mock_menu, mock_sys):
        admin = Admin()
        admin.admin_features()
        mock_sys.exit.assert_called_once()
        self.assertEqual(mock_print.call_count, 2)

    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    @mock.patch('aims.admin.input_validation')
    def test_create_employee(self, mock_validation, mock_db, mock_print, mock_input):
        mock_db().commit_data.side_effect = [sqlite3.IntegrityError, '']
        admin = Admin()
        admin.create_employee()
        self.assertEqual(2, mock_print.call_count)
        self.assertEqual(2, mock_db().create_employee.call_count)

    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    @mock.patch('aims.admin.input_validation')
    def test_create_employee_exception(self, mock_validation, mock_db, mock_print, mock_input):
        mock_db().commit_data.side_effect = Exception
        admin = Admin()
        admin.create_employee()
        self.assertEqual(1, mock_print.call_count)
        self.assertEqual(1, mock_db().create_employee.call_count)
        mock_db().rollback_data.assert_called_once()

    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.encrypt_pass')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    @mock.patch('aims.admin.input_validation')
    def test_update_employee_password(self, mock_validation, mock_db, mock_print, mock_input, mock_table_menu, mock_encrypt,  mock_menu):
        mock_db().worker_table_fields.return_value = []
        mock_menu().draw_menu.return_value = 'password'
        admin = Admin()
        admin.update_employee()
        mock_encrypt.assert_called_once()
        mock_db().update_member.assert_called_once()
        mock_db().commit_data.assert_called_once()

    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    @mock.patch('aims.admin.input_validation')
    def test_update_employee_email(self, mock_validation, mock_db, mock_print, mock_input, mock_table_menu, mock_menu):
        mock_db().worker_table_fields.return_value = []
        mock_menu().draw_menu.return_value = 'email'
        admin = Admin()
        admin.update_employee()
        mock_db().update_member.assert_called_once()
        mock_db().commit_data.assert_called_once()

    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    @mock.patch('aims.admin.input_validation')
    def test_update_employee_phone(self, mock_validation, mock_db, mock_print, mock_input, mock_table_menu, mock_menu):
        mock_db().worker_table_fields.return_value = []
        mock_menu().draw_menu.return_value = 'phone_number'
        admin = Admin()
        admin.update_employee()
        mock_db().update_member.assert_called_once()
        mock_db().commit_data.assert_called_once()

    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    def test_update_employee_others(self, mock_db, mock_print, mock_input, mock_table_menu, mock_menu):
        mock_db().worker_table_fields.return_value = []
        mock_menu().draw_menu.return_value = 'other_field'
        admin = Admin()
        admin.update_employee()
        mock_db().update_member.assert_called_once()
        mock_db().commit_data.assert_called_once()

    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    def test_update_employee_back_button(self, mock_db, mock_print, mock_input, mock_table_menu, mock_menu):
        mock_db().worker_table_fields.return_value = []
        mock_menu().draw_menu.return_value = 'BACK'
        admin = Admin()
        admin.update_employee()
        mock_print.assert_called_once()
        mock_input.assert_called_once()

    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('aims.admin.ConnectDb')
    def test_update_employee_no_emp(self, mock_db, mock_table_menu):
        mock_table_menu.return_value = None
        admin = Admin()
        admin.update_employee()
        mock_table_menu.assert_called_once()

    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    @mock.patch('aims.admin.input_validation')
    def test_update_employee_sqlite_exception(self, mock_validation, mock_db, mock_print, mock_input, mock_table_menu, mock_menu):
        mock_db().worker_table_fields.return_value = []
        mock_menu().draw_menu.return_value = 'email'
        mock_db().commit_data.side_effect = sqlite3.IntegrityError

        admin = Admin()
        admin.update_employee()
        mock_db().update_member.assert_called_once()

    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    @mock.patch('aims.admin.input_validation')
    def test_update_employee_exception(self, mock_validation, mock_db, mock_print, mock_input, mock_table_menu, mock_menu):
        mock_db().worker_table_fields.return_value = []
        mock_menu().draw_menu.return_value = 'email'
        mock_db().commit_data.side_effect = Exception

        admin = Admin()
        admin.update_employee()
        mock_db().update_member.assert_called_once()

    @mock.patch('aims.admin.ConnectDb')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('builtins.print')
    def test_delete_employee(self, mock_print, mock_table_menu, mock_db):
        admin = Admin()
        admin.delete_employee()
        mock_db().delete_member.assert_called_once()
        mock_db().delete_user_all_roles.assert_called_once()
        mock_db().commit_data.assert_called_once()

    @mock.patch('aims.admin.ConnectDb')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('builtins.print')
    def test_delete_employee_no_emp(self, mock_print, mock_table_menu, mock_db):
        mock_table_menu.return_value = None
        admin = Admin()
        admin.delete_employee()
        mock_db().show_members.assert_called_once()
        mock_table_menu.assert_called_once()

    @mock.patch('aims.admin.ConnectDb')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('builtins.print')
    def test_delete_employee_exception(self, mock_print, mock_table_menu, mock_db):
        mock_db().commit_data.side_effect = Exception
        admin = Admin()
        admin.delete_employee()
        mock_db().delete_member.assert_called_once()
        mock_db().delete_user_all_roles.assert_called_once()
        mock_db().rollback_data.assert_called_once()

    @mock.patch('aims.admin.raw_data_to_table')
    @mock.patch('aims.admin.ConnectDb')
    def test_show_final_reports(self, mock_db, mock_print_table):
        mock_db().show_final_reports().fetchall.return_value = [[1, 2, 3, '4', 5, '6']]
        admin = Admin()
        admin.show_final_reports()
        mock_print_table.assert_called_once()
        mock_db().show_final_reports.assert_called_once

    @mock.patch('aims.admin.Admin.add_supervisor')
    @mock.patch('aims.admin.Admin.remove_supervisor')
    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    def test_accident_complains_back(self, mock_db, mock_print, mock_input, mock_table_menu, mock_menu,
                                mock_remove_supervisor, mock_add_supervisor):
        mock_menu().draw_menu.return_value = 'BACK'
        admin = Admin()
        admin.accident_complains()
        mock_input.assert_called_once()
        mock_menu().draw_menu.assert_called_once()

    @mock.patch('aims.admin.Admin.add_supervisor')
    @mock.patch('aims.admin.Admin.remove_supervisor')
    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    def test_accident_complains_no_accident(self, mock_db, mock_print, mock_input, mock_table_menu, mock_menu,
                                     mock_remove_supervisor, mock_add_supervisor):
        mock_menu().draw_menu.return_value = 'NEW'
        mock_table_menu.return_value = None
        admin = Admin()
        admin.accident_complains()
        mock_input.assert_called_once()
        mock_menu().draw_menu.assert_called_once()

    @mock.patch('aims.admin.Admin.add_supervisor')
    @mock.patch('aims.admin.Admin.remove_supervisor')
    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    def test_accident_complains_wip_add(self, mock_db, mock_print, mock_input, mock_table_menu, mock_menu,
                                     mock_remove_supervisor, mock_add_supervisor):
        mock_menu().draw_menu.side_effect = ['WIP', 'ADD_SUPERVISOR']
        mock_table_menu.side_effect = ['', 'None']
        admin = Admin()
        admin.accident_complains()
        mock_add_supervisor.assert_called_once()

    @mock.patch('aims.admin.Admin.add_supervisor')
    @mock.patch('aims.admin.Admin.remove_supervisor')
    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    def test_accident_complains_wip_remove(self, mock_db, mock_print, mock_input, mock_table_menu, mock_menu,
                                             mock_remove_supervisor, mock_add_supervisor):
        mock_menu().draw_menu.side_effect = ['WIP', 'REMOVE_SUPERVISOR']
        mock_table_menu.side_effect = ['', 'None']
        admin = Admin()
        admin.accident_complains()
        mock_remove_supervisor.assert_called_once()

    @mock.patch('aims.admin.Admin.add_supervisor')
    @mock.patch('aims.admin.Admin.remove_supervisor')
    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    def test_accident_complains_wip_add_no_member(self, mock_db, mock_print, mock_input, mock_table_menu, mock_menu,
                                        mock_remove_supervisor, mock_add_supervisor):
        mock_menu().draw_menu.side_effect = ['WIP', 'ADD_SUPERVISOR']
        mock_table_menu.side_effect = ['', None]
        admin = Admin()
        admin.accident_complains()
        self.assertEqual(2, mock_table_menu.call_count)

    @mock.patch('aims.admin.Admin.add_supervisor')
    @mock.patch('aims.admin.Admin.remove_supervisor')
    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    def test_accident_complains_wip_remove_no_member(self, mock_db, mock_print, mock_input, mock_table_menu, mock_menu,
                                           mock_remove_supervisor, mock_add_supervisor):
        mock_menu().draw_menu.side_effect = ['WIP', 'REMOVE_SUPERVISOR']
        mock_table_menu.side_effect = ['', None]
        admin = Admin()
        admin.accident_complains()
        self.assertEqual(2, mock_table_menu.call_count)

    @mock.patch('aims.admin.ConnectDb')
    def test_remove_supervisor(self, mock_db):
        mock_db().check_supervisor_accident.return_value = False
        admin = Admin()
        admin.remove_supervisor(1, 1)
        mock_db().remove_supervisor_accident.assert_called_once()
        mock_db().check_supervisor_accident.assert_called_once()
        mock_db().remove_supervisor_role.assert_called_once()

    @mock.patch('aims.admin.ConnectDb')
    def test_remove_supervisor_exception(self, mock_db):
        mock_db().remove_supervisor_accident.side_effect = Exception
        admin = Admin()
        admin.remove_supervisor(1, 1)
        mock_db().remove_supervisor_accident.assert_called_once()
        mock_db().rollback_data.assert_called_once()

    @mock.patch('aims.admin.ConnectDb')
    def test_add_supervisor(self, mock_db):
        admin = Admin()
        admin.add_supervisor(1, 1)
        self.assertEqual(3, mock_db().commit_data.call_count)

    @mock.patch('aims.admin.ConnectDb')
    def test_add_supervisor_first_exception(self, mock_db):
        mock_db().commit_data.side_effect = ['', sqlite3.IntegrityError, '']
        admin = Admin()
        admin.add_supervisor(1, 1)
        self.assertEqual(3, mock_db().commit_data.call_count)

    @mock.patch('aims.admin.ConnectDb')
    def test_add_supervisor_second_exception(self, mock_db):
        mock_db().commit_data.side_effect = ['', '', sqlite3.IntegrityError]
        admin = Admin()
        admin.add_supervisor(1, 1)
        self.assertEqual(3, mock_db().commit_data.call_count)

    @mock.patch('aims.admin.ConnectDb')
    def test_add_supervisor_third_exception(self, mock_db):
        mock_db().change_accident_to_wip.side_effect = Exception
        admin = Admin()
        admin.add_supervisor(1, 1)
        mock_db().rollback_data.assert_called_once()

    @mock.patch('aims.admin.raw_data_to_table')
    @mock.patch('builtins.input')
    def test_show_table_menu(self, mock_input, mock_raw_table):
        cursor = MockCursor()
        admin = Admin()
        mock_input.return_value = '0'
        result = admin.show_table_menu(cursor, [1], [2])
        self.assertEqual(2, result)
        mock_raw_table.assert_called_once()

    @mock.patch('aims.admin.raw_data_to_table')
    @mock.patch('builtins.input')
    def test_show_table_menu_exception(self, mock_input, mock_raw_table):
        cursor = MockCursor()
        admin = Admin()
        mock_input.return_value = 'dummy'
        result = admin.show_table_menu(cursor, [1], [2])
        self.assertEqual(None, result)
        mock_raw_table.assert_called_once()

    @mock.patch('aims.admin.raw_data_to_table')
    @mock.patch('builtins.input')
    def test_show_table_menu_inout_out_of_index(self, mock_input, mock_raw_table):
        cursor = MockCursor()
        admin = Admin()
        mock_input.return_value = '2'
        result = admin.show_table_menu(cursor, [1], [2])
        self.assertEqual(None, result)
        mock_raw_table.assert_called_once()

    @mock.patch('aims.admin.ConnectDb')
    @mock.patch('aims.admin.raw_data_to_table')
    @mock.patch('builtins.input')
    def test_choose_multiple_employee(self, mock_input, mock_raw_table, mock_db):
        mock_db().show_members().fetchall.return_value = [[1, 2, 3]]
        mock_input.return_value = '0,1,2'
        admin = Admin()
        result = admin.choose_multiple_employee()
        assert result, [1]

    @mock.patch('aims.admin.ConnectDb')
    @mock.patch('aims.admin.raw_data_to_table')
    @mock.patch('builtins.input')
    def test_choose_multiple_employee_exception(self, mock_input, mock_raw_table, mock_db):
        mock_db().show_members().fetchall.return_value = [[1, 2, 3]]
        mock_input.return_value = 'asd,1,2'
        admin = Admin()
        result = admin.choose_multiple_employee()
        self.assertEqual(result, None)

    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    @mock.patch('aims.admin.raw_data_to_table')
    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('aims.admin.Admin.choose_multiple_employee')
    def test_manage_supervisor_reports_back(self, mock_choose_employee, mock_show_table, mock_menu, mock_raw_table, mock_db,
                                       mock_print, mock_input):
        mock_menu().draw_menu.return_value = 'BACK'
        admin = Admin()
        admin.manage_supervisor_reports()
        mock_menu().draw_menu.assert_called_once()

    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    @mock.patch('aims.admin.raw_data_to_table')
    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('aims.admin.Admin.choose_multiple_employee')
    def test_manage_supervisor_reports_resolved(self, mock_choose_employee, mock_show_table, mock_menu, mock_raw_table, mock_db,
                                       mock_print, mock_input):
        mock_menu().draw_menu.return_value = 'RESOLVED'
        admin = Admin()
        admin.manage_supervisor_reports()
        mock_menu().draw_menu.assert_called_once()
        mock_raw_table.assert_called_once()

    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    @mock.patch('aims.admin.raw_data_to_table')
    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('aims.admin.Admin.choose_multiple_employee')
    def test_manage_supervisor_reports_wip(self, mock_choose_employee, mock_show_table, mock_menu, mock_raw_table, mock_db,
                                       mock_print, mock_input):
        mock_menu().draw_menu.return_value = 'WIP'
        mock_choose_employee.return_value = ['1', '2']
        admin = Admin()
        admin.manage_supervisor_reports()
        mock_menu().draw_menu.assert_called_once()
        mock_db().commit_data.assert_called_once()
        mock_db().insert_finalize_report.assert_called_once()
        mock_db().close_accident_cases.assert_called_once()

    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    @mock.patch('aims.admin.raw_data_to_table')
    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('aims.admin.Admin.choose_multiple_employee')
    def test_manage_supervisor_reports_exception(self, mock_choose_employee, mock_show_table, mock_menu, mock_raw_table, mock_db,
                                       mock_print, mock_input):
        mock_menu().draw_menu.return_value = 'WIP'
        mock_db().commit_data.side_effect = Exception

        mock_choose_employee.return_value = ['1', '2']
        admin = Admin()
        admin.manage_supervisor_reports()
        mock_menu().draw_menu.assert_called_once()
        mock_db().rollback_data.assert_called_once()
        mock_db().insert_finalize_report.assert_called_once()
        mock_db().close_accident_cases.assert_called_once()


    @mock.patch('builtins.input')
    @mock.patch('builtins.print')
    @mock.patch('aims.admin.ConnectDb')
    @mock.patch('aims.admin.raw_data_to_table')
    @mock.patch('aims.admin.Menu')
    @mock.patch('aims.admin.Admin.show_table_menu')
    @mock.patch('aims.admin.Admin.choose_multiple_employee')
    def test_manage_supervisor_reports_wip_no_accident(self, mock_choose_employee, mock_show_table, mock_menu, mock_raw_table, mock_db,
                                       mock_print, mock_input):
        mock_menu().draw_menu.return_value = 'WIP'
        mock_show_table.return_value = None
        admin = Admin()
        admin.manage_supervisor_reports()
        mock_menu().draw_menu.assert_called_once()
        mock_db().show_status_accident_report.assert_called_once()


if __name__ == '__main__':
    unittest.main()
