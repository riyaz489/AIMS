import unittest
import mock
import sqlite3
from common.connect_db import ConnectDb


class DbConnectTest(unittest.TestCase):

    @mock.patch('common.connect_db.sys')
    @mock.patch('common.connect_db.sqlite3.connect', side_effect=sqlite3.Error)
    def test_db_connection_fail(self, mock_cursor, mock_sys):
        ConnectDb()
        mock_sys.exit.assert_called_once()

    @mock.patch('common.connect_db.yaml')
    @mock.patch('common.connect_db.sqlite3.connect')
    def test_db_connection(self, mock_cursor, mock_yaml):
        ConnectDb()
        mock_yaml.safe_load.assert_called_once()
        mock_cursor.assert_called_once()

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_db_script(self, mock_cursor):
        db = ConnectDb()
        db.db_script()

        mock_cursor().cursor().executescript.assert_called_once()
        mock_cursor().commit.assert_called_once()
        mock_cursor().cursor().close.assert_called_once()
        mock_cursor().close.assert_called_once()

    @mock.patch('common.connect_db.ConnectDb.commit_data', side_effect=sqlite3.Error)
    @mock.patch('common.connect_db.sys')
    @mock.patch('common.connect_db.sqlite3.connect')
    def test_db_script_fail(self, mock_cursor, mock_sys, mock_connect):
        db = ConnectDb()
        db.db_script()

        mock_sys.exit.assert_called_once()
        mock_cursor().cursor().close.assert_called_once()
        mock_cursor().rollback.assert_called_once()
        mock_cursor().close.assert_called_once()

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_close_conn(self, mock_cursor):
        # act
        db = ConnectDb()
        db.close_conn()
        # assert
        mock_cursor().cursor().close.assert_called_once()
        mock_cursor().close.assert_called_once()

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_commit_data(self, mock_cursor):
        # act
        db = ConnectDb()
        db.commit_data()
        # assert
        mock_cursor().commit.assert_called_once()

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_rollback_data(self, mock_cursor):
        # act
        db = ConnectDb()
        db.rollback_data()
        # assert
        mock_cursor().rollback.assert_called_once()


    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_user_info(self, mock_cursor):
        # arrange
        user_name = 'dummy'
        mock_cursor.cursor().execute().fetchone.return_value = 'dummy'
        # act
        db = ConnectDb()
        result = db.get_user_info(user_name)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [user_name])
        mock_cursor().cursor().execute().fetchone.assert_called_once()
        assert result, 'dummy'

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_user_role(self, mock_cursor):
        # arrange
        mock_cursor.cursor().execute().fetchone.return_value = 'dummy'
        # act
        db = ConnectDb()
        result = db.get_user_role(1, 1)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [1, 1])
        mock_cursor().cursor().execute().fetchone.assert_called_once()
        assert result, 'dummy'

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_accident_types(self, mock_cursor):
        # arrange
        mock_cursor.cursor().execute().fetchall.return_value = 'dummy'
        # act
        db = ConnectDb()
        result = db.get_accident_types()
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY)
        mock_cursor().cursor().execute().fetchall.assert_called_once()
        assert result, 'dummy'

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_report_new_accident(self, mock_cursor):
        # act
        db = ConnectDb()
        db.report_new_accident({})
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, {})

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_create_employee(self, mock_cursor):
        # act
        db = ConnectDb()
        db.create_employee({})
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, {})

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_show_members(self, mock_cursor):
        # act
        db = ConnectDb()
        result = db.show_members()
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY)

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_worker_table_feilds(self, mock_cursor):

        db = ConnectDb()
        db.worker_table_fields()
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY)

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_update_member(self, mock_cursor):
        # act
        db = ConnectDb()
        db.update_member(1, 'col', 1)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [1, 1])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_delete_member(self, mock_cursor):

        db = ConnectDb()
        db.delete_member(1)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [1])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_delete_user_all_roles(self, mock_cursor):

        db = ConnectDb()
        db.delete_user_all_roles(1)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY,[1])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_show_final_reports(self, mock_cursor):

        db = ConnectDb()
        db.show_final_reports()
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY)

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_fetch_emails(self, mock_cursor):
        # arrange
        mock_cursor.cursor().execute().fetchall.return_value = 'dummy'
        # act
        db = ConnectDb()
        result = db.fetch_emails(['1', '2'])
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, ['1', '2'])
        mock_cursor().cursor().execute().fetchall.assert_called_once()
        assert result, 'dummy'

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_show_status_accidents(self, mock_cursor):
        db = ConnectDb()
        db.show_status_accidents('status')
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, ['status'])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_add_accident_supervisor(self, mock_cursor):

        db = ConnectDb()
        db.add_accident_supervisor(1, 2)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [1, 2])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_add_supervisor_role(self, mock_cursor):
        # arrange
        mock_cursor.cursor().execute().fetchall.return_value = 'dummy'
        # act
        db = ConnectDb()
        db.add_supervisor_role(1)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [1, 1])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_change_accident_to_wip(self, mock_cursor):

        db = ConnectDb()
        db.change_accident_to_wip(1)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, ['WIP', 1])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_check_supervisor_accident(self, mock_cursor):
        # arrange
        mock_cursor.cursor().execute().fetchall.return_value = 'dummy'
        # act
        db = ConnectDb()
        result = db.check_supervisor_accident(1)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [1])
        mock_cursor().cursor().execute().fetchall.assert_called_once()
        assert result, 'dummy'

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_remove_supervisor_accident(self, mock_cursor):
        db = ConnectDb()
        db.remove_supervisor_accident(1, 1)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [1, 1])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_remove_supervisor_role(self, mock_cursor):
        db = ConnectDb()
        db.remove_supervisor_role(1)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [1, 1])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_get_accident_members(self, mock_cursor):
        # arrange
        mock_cursor.cursor().execute().fetchall.return_value = 'dummy'
        # act
        db = ConnectDb()
        result = db.get_accident_members(1)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [1])
        mock_cursor().cursor().execute().fetchall.assert_called_once()
        assert result, 'dummy'

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_show_status_accident_report(self, mock_cursor):
        db = ConnectDb()
        db.show_status_accident_report(1)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, [1])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_close_accident_cases(self, mock_cursor):
        db = ConnectDb()
        db.close_accident_cases(1)
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, ['RESOLVED', 1])

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_insert_finalize_report(self, mock_cursor):
        db = ConnectDb()
        db.insert_finalize_report({})
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, {})

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_show_supervisor_accidents(self, mock_cursor):
        # arrange
        mock_cursor.cursor().execute().fetchall.return_value = []
        # act
        db = ConnectDb()
        db.show_supervisor_accidents(1)
        # assert
        self.assertEqual(mock_cursor().cursor().execute.call_count, 2)
        mock_cursor().cursor().execute().fetchall.assert_called_once()

    @mock.patch('common.connect_db.sqlite3.connect')
    def test_register_supervisor_report(self, mock_cursor):
        db = ConnectDb()
        db.register_supervisor_report({})
        # assert
        mock_cursor().cursor().execute.assert_called_once_with(mock.ANY, {})


if __name__ == '__main__':
    unittest.main()
