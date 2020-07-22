import os
import sys
from common.constants import *
from common.helper import *
import datetime as d
import getpass
from common.connect_db import ConnectDb
from common.password_encryption import encrypt_pass
from common.validations import Validation
import sqlite3


class Admin:
    """this is a class for admin related operations."""

    def __init__(self):
        """
        initializing Employee class.
        """
        self.conn = ConnectDb()
        self.admin_id = ''

    def __del__(self):
        """
        closing database connection.
        """
        self.conn.close_conn()

    def admin_features(self):
        """
        this method is used to print all admin features on console.
        """
        try:
            while True:
                print("choose feature :\n")
                menu = Menu()
                features = [x.name for x in AdminFeatures]
                features.extend([str(BackButton.EXIT.name)])
                feature = menu.draw_menu(features)
                input()
                required_feature = getattr(self, feature.lower())
                required_feature()
                # again calling admin menu
                input()
                os.system('clear')
                self.admin_features()

        except Exception as e:
            print(e)
            sys.exit()

    def create_employee(self):
        """
        this method is used to register new employee in system.
        """
        user_dict = dict()
        user_dict['name'] = input('enter name of employee ')
        user_dict['password'] = input_validation("enter password for employee ", Validation.password, "Weak Password")
        user_dict['email'] = input_validation("enter email for employee ", Validation.is_email, "Invalid Email")
        user_dict['phone_number'] = input_validation("enter employee phone number ", Validation.is_phone,
                                                     "Invalid Phone Number")
        user_dict['created_at'] = d.datetime.now()
        user_dict['updated_at'] = d.datetime.now()
        user_dict['is_deleted'] = False
        user_dict['designation'] = input('enter designation of employee ')
        try:
            while True:
                user_dict['user_name'] = input('enter user_name for employee ')
                try:
                    self.conn.create_employee(user_dict)
                    self.conn.commit_data()
                    print(Color.F_Green, 'Record inserted', Base.END)
                    input()
                    break
                except sqlite3.IntegrityError:
                    print(Color.F_Red, 'user name is taken by some one else', Base.END)

        except Exception:
            print(Color.F_Red, 'some internal error occurred', Base.END)
            self.conn.rollback_data()

    def update_employee(self):
        """
        this method is used to update employee details.
        """
        cursor = self.conn.show_members()
        emp_id = self.show_table_menu(cursor)
        if emp_id is None:
            return
        columns = self.conn.worker_table_fields()
        print("choose attribute :\n")
        menu = Menu()
        columns.extend([str(BackButton.BACK.name), str(BackButton.EXIT.name)])
        column = menu.draw_menu(columns)
        input()
        user_input = ''
        if column == str(BackButton.BACK.name):
            return
        elif column == str(MemberUpdateColumns.password.name):
            user_input = encrypt_pass(input_validation("enter new value: ", Validation.password, 'Weak password'))
        elif column == str(MemberUpdateColumns.email.name):
            user_input = input_validation("enter new value: ", Validation.is_email, 'Invalid Email')
        elif column == str(MemberUpdateColumns.phone_number.name) and not Validation.is_phone(user_input):
            user_input = input_validation("enter new value: ", Validation.is_phone, "Invalid Phone Number")
        else:
            user_input = input("enter new value: ")
        try:
            self.conn.update_member(emp_id, column, user_input)
            self.conn.commit_data()
            print(Color.F_Red, 'Record Updated', Base.END)

        except sqlite3.IntegrityError:
            print(Color.F_Red, 'user_name already taken', Base.END)
        except Exception:
            print(Color.F_Red, 'some internal error occurred', Base.END)

    def delete_employee(self):
        """
        this method is used to delete employee details.
        """
        cursor = self.conn.show_members()
        emp_id = self.show_table_menu(cursor)
        if emp_id is None:
            return
        try:
            self.conn.delete_member(emp_id)
            self.conn.delete_user_all_roles(emp_id)
            self.conn.commit_data()
            print(Color.F_Red, 'Record Deleted', Base.END)

        except Exception:
            print(Color.F_Red, 'some internal error occurred', Base.END)
            self.conn.rollback_data()

    def show_final_reports(self):
        """
        this method is used to show final reports.
        """
        cursor = self.conn.show_final_reports()
        columns = [x[0] for x in cursor.description]
        data = [list(x) for x in cursor.fetchall()]
        for x in data:
            x[3] = [list(x)[0] for x in self.conn.fetch_emails(x[3].split(','))]
            x[5] = [list(x)[0] for x in self.conn.fetch_emails(x[5].split(','))]

        raw_data_to_table(columns, data)

    def accident_complains(self):
        """
        this method is used to see accident complains and also perform necessary actions to it.
        """
        flag = True
        options = [str(AccidentStatus.NEW.name), str(AccidentStatus.WIP.name), str(BackButton.BACK.name)]
        menu = Menu()
        column = menu.draw_menu(options)
        input()
        if column == str(BackButton.BACK.name):
            return
        cursor = ''
        if column == str(AccidentStatus.NEW.name):
            cursor = self.conn.show_status_accidents(str(AccidentStatus.NEW.name))
            flag = False
        if column == str(AccidentStatus.WIP.name):
            cursor = self.conn.show_status_accidents(str(AccidentStatus.WIP.name))

        accident_id = self.show_table_menu(cursor)
        if accident_id is None:
            return
        print('choose operation: \n')
        menu = Menu()
        options = [str(AdminSupervisorOperation.ADD_SUPERVISOR.name)]
        if flag:
            options.append(str(AdminSupervisorOperation.REMOVE_SUPERVISOR.name))

        supervisor_operation = menu.draw_menu(options)
        input()
        print('choose a supervisor for given accident')
        accident_supervisors = self.conn.get_accident_members(accident_id)
        accident_supervisors = [list(x)[0] for x in accident_supervisors]
        cursor = self.conn.show_members()
        if supervisor_operation == str(AdminSupervisorOperation.ADD_SUPERVISOR.name):
            member_id = self.show_table_menu(cursor, remove_ids=accident_supervisors)
            if member_id is None:
                return
            self.add_supervisor(accident_id, member_id)
        elif supervisor_operation == str(AdminSupervisorOperation.REMOVE_SUPERVISOR.name):
            member_id = self.show_table_menu(cursor, take_ids=accident_supervisors)
            if member_id is None:
                return
            self.remove_supervisor(accident_id, member_id)

    def remove_supervisor(self, accident_id, member_id):
        """
        this method is used to remove supervisor from given project.
        :param accident_id: string, accident id
        :param member_id: string, member id
        """
        try:
            self.conn.remove_supervisor_accident(member_id, accident_id)
            self.conn.commit_data()
            if not self.conn.check_supervisor_accident(member_id):
                self.conn.remove_supervisor_role(member_id)
            self.conn.commit_data()
            print(Color.F_Green, 'record changed', Base.END)
        except:
            print(Color.F_Red, 'some internal error occurred', Base.END)
            self.conn.rollback_data()

    def add_supervisor(self, accident_id, member_id):
        """
        this method is used to add supervisor to given project.
        :param accident_id: string, accident id
        :param member_id: string, member id
        """
        try:
            try:
                self.conn.change_accident_to_wip(accident_id)
                self.conn.commit_data()
                self.conn.add_accident_supervisor(accident_id, member_id)
                self.conn.commit_data()
            except sqlite3.IntegrityError:
                pass
            try:
                self.conn.add_supervisor_role(member_id)
                self.conn.commit_data()
                print(Color.F_Green, 'record inserted', Base.END)
            except sqlite3.IntegrityError:
                print(Color.F_Green, 'record inserted', Base.END)
        except:
            print(Color.F_Red, 'some internal error occured', Base.END)
            self.conn.rollback_data()

    def show_table_menu(self, cursor, remove_ids=[-1], take_ids=[-1]):
        """
        this method is used to select employee/accidents from existing data.
        :param: cursor, data cursor.
        :param: list, ids to be removed from cursor data.
        :return: int, employee/accident id.
        """
        counter = 0
        actual_data = [list(elem) for elem in cursor.fetchall()]
        if remove_ids != [-1]:
            actual_data = list(filter(lambda x: x[0] not in remove_ids, actual_data))
        if take_ids != [-1]:
            actual_data = list(filter(lambda x: x[0] in take_ids, actual_data))
        raw_data = list()
        for elem in actual_data:
            temp = list(elem)[1:]
            temp.insert(0, counter)
            raw_data.append(temp)
            counter += 1
        field_names = [column[0] for column in cursor.description][1:]
        field_names.insert(0, 'index')
        raw_data_to_table(field_names, raw_data)
        index = input('write index to choose record: ')
        try:
            index = int(index)
            if 0 <= index < len(raw_data):
                return actual_data[index][0]
            else:
                print('wrong choice')
                return None
        except Exception as e:
            print('wrong choice')
            return None

    def choose_multiple_employee(self):
        """
        this method is used to choose multiple employees.
        :return: list, employees list
        """
        cursor = self.conn.show_members()
        counter = 0
        actual_data = [list(elem) for elem in cursor.fetchall()]
        raw_data = list()
        for elem in actual_data:
            temp = list(elem)[1:]
            temp.insert(0, counter)
            raw_data.append(temp)
            counter += 1
        field_names = [column[0] for column in cursor.description][1:]
        field_names.insert(0, 'index')
        raw_data_to_table(field_names, raw_data)
        index = input('write comma separated indexes to choose multiple records: ')
        temp = list()
        try:
            for x in index.split(','):
                x = int(x)
                if 0 <= x < len(raw_data):
                    temp.append(str(actual_data[x][0]))
            return temp
        except Exception as e:
            print('wrong choice')
            return None

    def manage_supervisor_reports(self):
        """
        this method is used to manage all supervisor reports.
        """
        options = [str(AccidentStatus.WIP.name), str(AccidentStatus.RESOLVED.name), str(BackButton.BACK.name)]
        menu = Menu()
        column = menu.draw_menu(options)
        input()
        if column == str(BackButton.BACK.name):
            return
        if column == str(AccidentStatus.RESOLVED.name):
            cursor = self.conn.show_status_accident_report(str(AccidentStatus.RESOLVED.name))
            raw_data_to_table([list(x)[0] for x in cursor.description], [list(x) for x in cursor.fetchall()])
        elif column == str(AccidentStatus.WIP.name):
            cursor = self.conn.show_status_accident_report(str(AccidentStatus.WIP.name))
            print('choose to finalize report (for any accident choose any record with similar accident id)')
            accident_id = self.show_table_menu(cursor)
            if accident_id is None:
                return
            print('choose victims')
            victims = self.choose_multiple_employee()
            print('choose culprit')
            culprit = self.choose_multiple_employee()
            temp_dict = dict()
            temp_dict['victims'] = ''
            temp_dict['culprit'] = ''
            if culprit != [] and culprit != None:
                temp_dict['culprit'] = ','.join(culprit)
            if victims != [] and victims != None:
                temp_dict['victims'] = ','.join(victims)
            temp_dict['location'] = input('write accident location: ')
            temp_dict['submission_time'] = d.datetime.now()
            temp_dict['time_of_accident'] = input('write time of accident ')
            temp_dict['action_to_resolve'] = input('write action to resolve ')
            temp_dict['reason'] = input('write accident reason ')
            temp_dict['accident_id'] = accident_id
            try:
                self.conn.close_accident_cases(accident_id)
                self.conn.insert_finalize_report(temp_dict)
                self.conn.commit_data()
                print('record inserted')
            except Exception as e:
                self.conn.rollback_data()
                print('some internal error occurred')
                print(e)
