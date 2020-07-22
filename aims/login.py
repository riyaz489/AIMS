""" this file is used to perform login related operations."""
from aims.supervisor import Supervisor
from common.constants import *
from common.helper import Menu
from common.connect_db import ConnectDb
from getpass import getpass
from common.password_encryption import decrypt_pass
import os
from aims.employee import Employee
from aims.admin import Admin
import sys


def main():
    """
    this method is used to call main menu for login
    """
    conn = ConnectDb()
    try:
        os.system('clear')
        # select role for login
        print("login as:\n")
        menu = Menu()
        roles = [x.name for x in Role]
        roles.extend([str(BackButton.EXIT.name)])
        role = menu.draw_menu(roles)
        role_id = Role[role].value
        input()

        # get user name and password for login
        user_name = input("enter user name: ")
        password = getpass()

        # check user authentication
        result = conn.get_user_info(user_name)
        flag = True
        auth_flag = True
        if result is not None:
            os.system('clear')
            actual_pass = decrypt_pass(result[1].encode())
            if actual_pass == password:
                flag = False
                if role_id == int(Role.EMPLOYEE.value):
                    auth_flag = False
                    emp = Employee()
                    emp.employee_id = result[0]
                    emp.employee_features()
                else:
                    user_role = conn.get_user_role(result[0], role_id)
                    if user_role is not None:
                        auth_flag = False
                        if role_id == int(Role.SUPERVISOR.value):
                            pass
                            supervisor = Supervisor()
                            supervisor.supervisor_id = result[0]
                            supervisor.supervisor_features()
                        elif role_id == int(Role.ADMIN.value):
                            pass
                            member = Admin()
                            member.admin_id = result[0]
                            member.admin_features()
        if flag:
            print(Color.F_Red + 'wrong credentials' + Base.END)
            input()
            main()
        if auth_flag:
            print(Color.F_Red + 'you are not authorized' + Base.END)
            input()
            main()

    except Exception as e:
        print(e)
        sys.exit()
    finally:
        conn.close_conn()


if __name__ == '__main__':
    """
    creating db schema and calling main function
    """
    con = ConnectDb()
    con.db_script()
    main()







