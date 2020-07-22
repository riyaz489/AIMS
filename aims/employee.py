import os
import sys
from common.constants import *
from common.helper import Menu
import datetime as d
from common.connect_db import ConnectDb


class Employee:
    """this is a class for employee related operations."""
    def __init__(self):
        """
        initializing Employee class.
        """
        self.conn = ConnectDb()
        self.employee_id = ''

    def __del__(self):
        """
        closing database connection.
        """
        self.conn.close_conn()

    def employee_features(self):
        """
        this method is used to print all employee features on console.
        """
        try:
            while True:
                supervisor_role = self.conn.get_user_role(self.employee_id, Role.SUPERVISOR.value)
                if supervisor_role is not None:
                    print(Color.F_Red, '\nYou are supervisor also.', Base.END)
                    print(Color.F_Red, 'for more info contact admin.', Base.END)
                print("choose feature :\n")
                menu = Menu()
                features = [x.name for x in MemberFeatures]
                features.extend([str(BackButton.EXIT.name)])
                feature = menu.draw_menu(features)
                input()
                required_feature = getattr(self, feature.lower())
                required_feature()
                # again calling employee menu
                input()
                os.system('clear')
                self.employee_features()

        except Exception as e:
            print(e)
            sys.exit()

    def file_complain(self):
        """
        this method is used to file complain.
        """
        accident_types = self.conn.get_accident_types()
        accident_types_list = [x[1] for x in accident_types]
        menu = Menu()
        print("\n Choose accident type: \n")
        accident_types_list.extend([str(BackButton.BACK.name), str(BackButton.EXIT.name)])
        accident_type = menu.draw_menu(accident_types_list)
        input()
        os.system('clear')
        if accident_type == str(BackButton.BACK.name):
            return
        accident_id = [x[0] for x in accident_types if x[1] == accident_type]
        location = input('enter accident location: ')
        complain_dict = dict()
        complain_dict['type'] = accident_id[0]
        complain_dict['timestamp'] = d.datetime.now()
        complain_dict['created_by'] = self.employee_id
        complain_dict['location'] = location
        complain_dict['status'] = AccidentStatus.NEW.name
        try:
            self.conn.report_new_accident(complain_dict)
            self.conn.commit_data()
            print("\n" + Color.F_Green + "record inserted" + Base.END)
        except Exception as e:
            print("\n" + Color.F_Red + "some exception occurred" + Base.END)
            print("reason:", e)
