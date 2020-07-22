""" this class is used to provide input validation"""
import re
from dateutil import parser


class Validation:

    @staticmethod
    def is_phone(user_input):
        """
        used to validate phone number.
        :param user_input: string, phone number.
        :return: bool, number is valid or not.
        """
        try:
            if len(user_input) == 10:
                int(user_input)
                return True
            return False
        except:
            return False

    @staticmethod
    def is_email(email):
        """
        this function is used to validate email.
        :param email: string, email string.
        :return: bool, email is valid or not.
        """
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if re.search(regex, email):
            return True
        else:
            return False

    @staticmethod
    def password(password):
        """
        this function is used to validate password
        :param password: string, user input password
        :return: bool, password is valid or not.
        """
        if len(password) < 8:
            return False
        elif not re.search("[a-z]", password):
            return False
        elif not re.search("[A-Z]", password):
            return False
        elif not re.search("[0-9]", password):
            return False
        elif not re.search("[_@$]", password):
            return False
        elif re.search("\s", password):
            return False
        else:
            return True


