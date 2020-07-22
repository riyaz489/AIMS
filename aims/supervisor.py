import os
import sys
from common.connect_db import ConnectDb
from common.constants import *
from common.helper import Menu
from aims.admin import Admin
import datetime as d


class Supervisor:
    """this is a class for supervisor related operations."""

    def __init__(self):
        """
        initializing supervisor class.
        """
        self.conn = ConnectDb()
        self.supervisor_id = ''

    def __del__(self):
        """
        closing database connection.
        """
        self.conn.close_conn()

    def supervisor_features(self):
        """
        this method is used to print all supervisor features on console.
        """
        try:
            while True:
                print("choose feature :\n")
                menu = Menu()
                features = [x.name for x in SupervisorFeatures]
                features.extend([str(BackButton.EXIT.name)])
                feature = menu.draw_menu(features)
                input()
                required_feature = getattr(self, feature.lower())
                required_feature()
                # again calling supervisor menu
                input()
                os.system('clear')
                self.supervisor_features()

        except Exception as e:
            print(e)
            sys.exit()

    def show_accident_complain(self):
        """
        this method is used to show supervisor accident complain.
        """
        cursor = self.conn.show_supervisor_accidents(self.supervisor_id)
        admin = Admin()
        temp_dict = dict()
        print('choose accident to send report')
        temp_dict['accident_id'] = admin.show_table_menu(cursor)
        if temp_dict['accident_id'] is None:
            return
        cursor = self.conn.show_members()
        print('choose eye witness')
        temp_dict['eye_witness'] = admin.show_table_menu(cursor)
        print('choose victims')
        victims = admin.choose_multiple_employee()
        print('choose culprit')
        temp_dict['victims'] = ''
        temp_dict['culprit'] = ''
        culprit = admin.choose_multiple_employee()
        if culprit != [] and culprit != None:
            temp_dict['culprit'] = ','.join(culprit)
        if victims != [] and victims != None:
            temp_dict['victims'] = ','.join(victims)
        temp_dict['submitted_by'] = self.supervisor_id
        temp_dict['reason'] = input('enter reason ')
        temp_dict['timing'] = input('enter accident timing ')
        temp_dict['submission_time'] = d.datetime.now()
        temp_dict['location'] = input('enter location of accident ')
        temp_dict['action_to_resolve'] = input('enter action to resolve ' )
        try:
            self.conn.register_supervisor_report(temp_dict)
            self.conn.commit_data()
            print('report submitted successfully.')
        except Exception as e:
            print('some error occured')
            print(e)
            self.conn.rollback_data()