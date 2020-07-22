""" this file is used to define constants, which are used in this project."""

import enum


class BackButton(enum.Enum):
    """
    This is used to provide constants for menu back buttons and exit button functionality.
    """
    BACK = 1
    EXIT = 2
    SIGN_OUT = 3


class Role(enum.Enum):
    """This is used to provide constants for different roles in the project."""
    # Accident supervisor
    SUPERVISOR = 1
    # AIMS admin
    ADMIN = 2
    # employees
    EMPLOYEE = 3


class MemberFeatures(enum.Enum):
    """This is used to provide constants for different features of Employees."""
    FILE_COMPLAIN = 1


class SupervisorFeatures(enum.Enum):
    """This is used to provide constants for different features of Supervisors."""
    SHOW_ACCIDENT_COMPLAIN = 1


class AdminFeatures(enum.Enum):
    """This is used to provide constants for different features of Admin."""
    CREATE_EMPLOYEE = 1
    ACCIDENT_COMPLAINS = 2
    MANAGE_SUPERVISOR_REPORTS = 3
    SHOW_FINAL_REPORTS = 4
    UPDATE_EMPLOYEE = 5
    DELETE_EMPLOYEE = 6


class MemberUpdateColumns(enum.Enum):
    """This is used to provide constants for different columns of worker table."""
    password = 1
    user_name = 2
    email = 3
    phone_number = 4
    name = 5
    designation = 6


class AccidentStatusMenu(enum.Enum):
    """This is used to provide constants for different report status for menu."""
    NEW_COMPLAINS = 1
    WIP_COMPLAINS = 2
    RESOLVED_COMPLAINS = 3


class AccidentStatus(enum.Enum):
    """This is used to provide constants for different report status."""
    NEW = 1
    WIP = 2
    RESOLVED = 3


class AdminSupervisorOperation(enum.Enum):
    """This is used to provide constants for add/remove supervisor."""
    ADD_SUPERVISOR = 1
    REMOVE_SUPERVISOR = 2


class Base:
    """this class is used to define constants for console formatting."""
    # Formatting
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    # End colored text
    END = '\033[0m'
    # No Color
    NC = '\x1b[0m'


class Color:
    """this class is used to define constants for console coloring."""

    # Foreground
    F_Default = "\x1b[39m"
    F_Black = "\x1b[30m"
    F_Red = "\x1b[31m"
    F_Green = "\x1b[32m"
    F_Yellow = "\x1b[33m"
    F_Blue = "\x1b[34m"
    F_Magenta = "\x1b[35m"
    F_Cyan = "\x1b[36m"
    F_LightGray = "\x1b[37m"
    F_DarkGray = "\x1b[90m"
    F_LightRed = "\x1b[91m"
    F_LightGreen = "\x1b[92m"
    F_LightYellow = "\x1b[93m"
    F_LightBlue = "\x1b[94m"
    F_LightMagenta = "\x1b[95m"
    F_LightCyan = "\x1b[96m"
    F_White = "\x1b[97m"

    # Background
    B_Default = "\x1b[49m"
    B_Black = "\x1b[40m"
    B_Red = "\x1b[41m"
    B_Green = "\x1b[42m"
    B_Yellow = "\x1b[43m"
    B_Blue = "\x1b[44m"
    B_Magenta = "\x1b[45m"
    B_Cyan = "\x1b[46m"
    B_LightGray = "\x1b[47m"
    B_DarkGray = "\x1b[100m"
    B_LightRed = "\x1b[101m"
    B_LightGreen = "\x1b[102m"
    B_LightYellow = "\x1b[103m"
    B_LightBlue = "\x1b[104m"
    B_LightMagenta = "\x1b[105m"
    B_LightCyan = "\x1b[106m"
    B_White = "\x1b[107m"
