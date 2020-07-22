""" this file is used to perform helper methods."""

import os
import sys
from prettytable import PrettyTable
from common.constants import Color, Base, BackButton
from pynput.keyboard import Key, Listener

from common.validations import Validation


def always_true():
    """ this method is used for infinite loops, so that later while unit testing we can set it false"""
    return True


def raw_data_to_table(cols, rows):
    """
    this method is used to print table form list/tuple data.
    :param cols: list, list of columns.
    :param rows: list, list of rows.
    """
    table = PrettyTable()
    table.field_names = cols
    for row in rows:
        table.add_row(row)
    print(table)


def input_validation(prompt, validation, error_msg):
    """
    this method is used to receive input until input is correct.
    :param prompt: string, input message.
    :param validation: validation, validation method
    :param error_msg: string, error message
    :return: validated data
    """
    while True:
        temp = input(prompt)
        if validation(temp):
            return temp
        else:
            print(Color.F_Red, error_msg, Base.END)


class Menu:
    """
       This is a class for printing menu for given list.

       Attributes:
           index (int): index of cursor.
           count (int): count of elements in list.
           flag (int): flag to exit from menu.
    """
    def __init__(self):
        """
        initializing menu attributes.
        """
        self.index = 0
        self.count = 0
        self.flag = 0

    def on_press(self, key):
        """
        this method is used to change index and flag attributes on the basis of user keyboard press.
        :param key: Key, keyboard pressed key.
        :return: bool, False.
        """
        try:
            if 'up' == key.name:
                if self.index > 0:
                    self.index -= 1
                else:
                    self.index = self.count
            elif 'down' == key.name:
                if self.index < self.count:
                    self.index += 1
                else:
                    self.index = 0
            elif key == Key.enter:
                # Stop listener
                self.flag += 1
            return False
        except:
            return False

    def draw_menu(self, items):
        """
        this method is used to print items on console and return the selected item.
        :param items: list, items to print on menu.
        :return: string, selected item name from menu.
        """

        self.count = len(items) - 1
        while True:
            if self.flag >= 1:
                if items[self.index] == str(BackButton.EXIT.name):
                    print("exiting from system")
                    sys.exit()
                else:

                    return items[self.index]

            for x in range(0, self.count+1):
                if x == self.index:
                    print(Color.B_LightGray + Color.F_Black + items[x] + Base.END)
                elif x == self.count:
                    print(Color.F_Red + items[x] + Base.END)
                else:
                    print(items[x])
            with Listener(
                    on_press=self.on_press
                   ) as listener:
                listener.join()

            os.system('clear')

            # providing if statement in last to emulate do while loop
            if not always_true():
                break
