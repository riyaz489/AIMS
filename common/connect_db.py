""" this file is used to perform database related operations."""

import sqlite3
import yaml
import sys
from common.constants import *


class ConnectDb:
    """ this is a class for database related operations.
        Attributes:
            conn (sqlite connection): connection object.
            cur (connection cursor): cursor object.
    """
    def __init__(self):
        """sqlite connection initialization."""
        try:
            with open("aims/config.yaml", 'r') as yaml_file:
                cfg = yaml.safe_load(yaml_file)
                db_path = cfg['mysql']['db']
                conn = sqlite3.connect(db_path)
        except sqlite3.Error as e:
            print(e)
            sys.exit()
        else:
            self.conn = conn
            self.cur = self.conn.cursor()

    def close_conn(self):
        """this method is used to close connection and cursor object."""
        self.cur.close()
        self.conn.close()

    def commit_data(self):
        """this method is used to commit changes on connection."""
        self.conn.commit()

    def rollback_data(self):
        """this method is used to rollback changes on connection ."""
        self.conn.rollback()

    def db_script(self):
        """this method is used to create schema for aims project. """
        try:
            with open('data/schema_script.sql', 'r') as sql_file:
                sql_script = sql_file.read()
                self.cur.executescript(sql_script)
                self.commit_data()

        except sqlite3.Error as error:
            print('unable to run database script')
            print(error)
            self.rollback_data()
            sys.exit()
        finally:
            self.close_conn()

    def get_user_info(self, user_name):
        """
        this method is used to get user info for login purpose.
        :param user_name: string, user name.
        :return: list, user details.
        """
        query = "select id, password from worker where is_deleted=0 and user_name =? "
        return self.cur.execute(query, [user_name]).fetchone()

    def get_accident_types(self):
        """
        this method is used to get all accident types.
        :return: list, accident types list.
        """
        query = "select * from accident_type"
        return self.cur.execute(query).fetchall()

    def report_new_accident(self, parameters_dict):
        """
        this method is used to add new accident details.
        :param parameters_dict: dictionary, contains new accident information.
        """
        query = " insert into accident (type, timestamp, created_by, location, status) values" \
                " (  :type, :timestamp, :created_by, :location, :status)"
        self.cur.execute(query, parameters_dict)

    def get_user_role(self, user_id, role_id):
        """
        this method is used to get user role information.
        :param user_id: sting, user id.
        :param role_id: string, role id.
        :return: list, return user role information.
        """
        query = "select * from user_role where user_id = ? and role=?"
        return self.cur.execute(query, [user_id, role_id]).fetchone()

    def create_employee(self, employee_dict):
        """
        this method is used to create new employee.
        :param employee_dict: dict, employee details.
        """
        "CREATE TABLE `worker` "
        query = 'insert into worker (password, user_name, email, phone_number, name, created_at, updated_at, ' \
                'is_deleted, designation ) values(:password, :user_name, :email, :phone_number, :name, :created_at,' \
                ' :updated_at, :is_deleted, :designation )'
        self.cur.execute(query, employee_dict)

    def show_members(self):
        """
        this method is used to show employee details.
        :return: list, list of employees.
        """
        query = "select id, user_name, email, name, created_at, updated_at, designation  from worker where " \
                "is_deleted=0"
        return self.cur.execute(query)

    def worker_table_fields(self):
        """
        this method is used to show columns in worker table.
        :return: list, list of columns.
        """
        query = "select password, user_name, email, phone_number, name, designation from worker limit 1"
        temp = self.cur.execute(query).description
        return [x[0] for x in temp]

    def update_member(self, member_id, column, new_value):
        """
        this method is used to update worker table record.
        :param member_id: string, member id.
        :param column: string, column name.
        :param new_value: string, new value for given column and member.
        """
        query = "update worker set "+column+" =? where id =?"
        self.cur.execute(query, [new_value, member_id])

    def delete_member(self, member_id):
        """
        this method is used to delete worker from table.
        :param member_id: string, member id.

        """
        query = "update worker set is_deleted =1 where id =?"
        self.cur.execute(query, [member_id])

    def delete_user_all_roles(self, member_id):
        """
        this method is used to delete all roles of given user.
        :param member_id: string,member id.
        """
        query = "delete from user_role where user_id = ?"
        self.cur.execute(query, [member_id])

    def show_final_reports(self):
        """this method is used to show final reports.
        :return list, list of final accident reports.
        """
        query = 'select type, name as created_by, accident_location, victims, time_of_accident, culprit,' \
                ' action_to_resolve, reason from final_accident_report as f inner join accident as a on ' \
                'a.id = f.accident_id inner join worker as w on w.id = a.created_by'
        return self.cur.execute(query)

    def fetch_emails(self, ids_list):
        """
        this method is used to fetch workers emails
        :param ids_list: list, worker ids list
        :return:list, list of emails
        """
        query = "select email from worker where id in (%s)" % ','.join('?'*len(ids_list))
        return self.cur.execute(query, ids_list).fetchall()

    def show_status_accidents(self, status):
        """
        this method is used to show new reports.
        :return list, list of new accident.
        """
        query = "select * from accident where status = ?"
        return self.cur.execute(query, [status])

    def add_accident_supervisor(self, accident_id, member_id):
        """
        this method is used to add new supervisor for given accident.
        :param accident_id: int, accident id
        :param member_id: int, member id
        """
        query = "insert into accidents_supervisor(`accident_id`, `supervisor_id`) values (?,?)"
        self.cur.execute(query, [accident_id, member_id])

    def add_supervisor_role(self, member_id):
        """
        this method is used to add new supervisor for given accident.
        :param member_id: int, member id
        """
        query = "insert into user_role(`user_id`, `role`) values (?,?)"
        self.cur.execute(query,  [member_id, int(Role.SUPERVISOR.value)])

    def change_accident_to_wip(self, accident_id):
        """
        this method is used to change accident status to work in progress.
        :param accident_id: string, accident id
        """
        query = "update accident set status = ? where id=?"
        self.cur.execute(query, [str(AccidentStatus.WIP.name), accident_id])

    def check_supervisor_accident(self, supervisor_id):
        """
        this method is used to check if any accident still exists under current supervisor
        :param supervisor_id:
        :return: list, supervisor_accident list
        """
        query = "select * from accidents_supervisor where supervisor_id=?"
        return self.cur.execute(query, [supervisor_id]).fetchall()

    def remove_supervisor_accident(self, supervisor_id, accident_id):
        """
        this method is used to remove supervisor from current accident.
        :param supervisor_id: string, supervisor id
        :param accident_id: string, accident id
        """
        query = "delete from accidents_supervisor where supervisor_id=? and accident_id =?"
        self.cur.execute(query, [supervisor_id, accident_id])

    def remove_supervisor_role(self, supervisor_id):
        """
        this method is used to remove supervisor from current accident.
        :param supervisor_id: string, supervisor id
        """
        query = "delete from user_role where user_id=? and role = ?"
        self.cur.execute(query, [supervisor_id, int(Role.SUPERVISOR.value)])

    def get_accident_members(self, accident_id):
        """
        this method is used to get supervisors for current accident.
        :param accident_id: string, accident id
        :return: list, list of supervisors ids
        """
        query = "select supervisor_id from accidents_supervisor where accident_id = ?"
        return self.cur.execute(query, [accident_id]).fetchall()

    def show_status_accident_report(self, status):
        """
        this method is used to get accident report for given status.
        :param status: string, accident status.
        :return: list, list of accident reports.
        """
        query = "select `accident_id`, accident_id as accident, `type`,w.name as submitted_by ,w2.name as eye_witness , `reason` , `timing`, " \
                "`submission_time`,a.location as location, casualties , `culprit` , `action_to_resolve` from accident_reports " \
                " as a inner join worker as w on w.id = a.submitted_by left join worker as w2 on w2.id = a.eye_witness" \
                " inner join accident a2 on a2.id=a.accident_id where status = ? order by timing, submission_time"
        return self.cur.execute(query, [status])

    def close_accident_cases(self, accident_id):
        """
        this method is used to close all accident cases.
        :param accident_id: string, accident id.
        """
        query = "update accident set status = ? where id =?"
        self.cur.execute(query, [str(AccidentStatus.RESOLVED.name), accident_id])

    def insert_finalize_report(self, dict_data):
        """
        this method is used to generate finalize report.
        :param dict_data: dict, accident details.
        """
        query = 'insert into final_accident_report (`accident_id`, `accident_location`, `victims`, `time_of_accident` ' \
                ', `submission_time`, `culprit`, `action_to_resolve`,`reason`  ) values(:accident_id,  :location, ' \
                ':victims, :time_of_accident, :submission_time, :culprit, :action_to_resolve, :reason)'
        self.cur.execute(query, dict_data)

    def show_supervisor_accidents(self, supervisor_id):
        """
        this method is used to show all accidents under current supervisor.
        :param supervisor_id: string, supervisor id .
        :return: list, supervisor accidents list.
        """
        query = "select accident_id from accidents_supervisor where supervisor_id = ?"
        temp = self.cur.execute(query, [supervisor_id]).fetchall()
        temp = [list(x)[0] for x in temp]
        query2 = "select a.id, at.accident as type, timestamp, name as created_by, location, status from accident as a " \
                 "inner join  worker as w on w.id = a.created_by inner join accident_type as at on at.id= " \
                 "a.type where status='WIP' and a.id in (%s)" % ','.join('?'*len(temp))
        return self.cur.execute(query2, temp)

    def register_supervisor_report(self, data_dict):
        """
        this method is used to add supervisor report to database.
        :param data_dict: dict, data dictionary.
        """
        query = "insert into accident_reports (accident_id, submitted_by, eye_witness, reason, timing, submission_time," \
                " location, casualties, culprit, action_to_resolve) values(:accident_id, :submitted_by, :eye_witness, " \
                ":reason, :timing, :submission_time, :location, :victims, :culprit, :action_to_resolve)"
        return self.cur.execute(query, data_dict)