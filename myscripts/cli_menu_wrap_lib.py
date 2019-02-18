from myscripts import cli_menu
import ipaddress
from myscripts import database_op


def add_ip_to_monitoring_menu(popen_list: dict, command: list) -> None:
    if len(command) == 3 or len(command) == 4:
        try:
            if len(command) == 3:
                session = database_op.IpSession(command[1], command[2])
            else:
                session = database_op.IpSession(command[1], command[2], command[3])
            cli_menu.add_ip_to_monitoring(session, popen_list)
        except ipaddress.AddressValueError:
            print("You put incorrect ip address {} after add".format(command[1]))
        except ValueError:
            print("You put incorrect ping interval {}".format(command[2]))
    else:
        print("You should put ip address after word add then interval in seconds.")
        print("You can also put hostname after ip address interval.")
        print("Print help and press Enter for more information.\n")


def del_ip_from_monitoring_menu(popen_list: dict, command: list) -> None:
    if len(command) == 2:
        cli_menu.remove_ip_from_monitoring(command[1], popen_list)
    else:
        print("You should put ip address after word del.")
        print("Print help and press Enter for more information.\n")


def import_ip_from_ip_file_list_menu(popen_list: dict, command: list) -> None:  #!!!!!!!!
    if len(command) == 1:
        ipexportlist = cli_menu.import_ip_from_file()
        if len(ipexportlist) > 0:
            for ip in ipexportlist:
                ip, interval, hostname = database_op.extract_parameters_of_ip_session_ipsessions_table(ip)
                session = database_op.IpSession(ip, interval, hostname)
                cli_menu.add_ip_to_monitoring(session, popen_list)
        else:
            print("No ips was extracted from database, nothing will be added to monitoring.")
    else:
        print("You should not put any words after import.")
        print("Print help and press Enter for more information.\n")


def show_ip_in_monitoring_menu(popen_list: dict, command: list) -> None:
    # command is not used here, it is here to simplify method list wrapper
    if len(command) == 1:
        cli_menu.show_ip_in_monitoring(popen_list)
    else:
        print("You should not put any words after show.")
        print("Print help and press Enter for more information.\n")


def give_help_menu_menu(popen_list: dict, command: list) -> None:
    # command and popen_list is not used here, it is here to simplify method list wrapper
    if len(command) == 1:
        cli_menu.give_help_menu()
    else:
        print("You should not put any words after help.")
        print("Print help and press Enter for more information.\n")


def exit_program_menu(popen_list: dict, command: list) -> None:
    # command is not used here, it is here to simplify method list wrapper
    if len(command) == 1:
        cli_menu.exit_program(popen_list)
    else:
        print("You should not put any words after exit.")
        print("Print help and press Enter for more information.\n")


def setup_menu(popen_list: dict, command: list) -> None:
    if len(command) == 1:
        cli_menu.setup()
    else:
        print("You should not put any words after exit.")
        print("Print help and press Enter for more information.\n")


def make_email_recipient_list_menu(popen_list: dict, command: list) -> None:
    if len(command) == 1:
        cli_menu.make_email_recipient_list()
    else:
        print("You should not put any words after recipients.")
        print("Print help and press Enter for more information.\n")

# This is wrapper  which is used in main.py file
menu_wrapper = {
    "recipients": make_email_recipient_list_menu,
    "setup": setup_menu,
    "add": add_ip_to_monitoring_menu,
    "del": del_ip_from_monitoring_menu,
    "import": import_ip_from_ip_file_list_menu,
    "show": show_ip_in_monitoring_menu,
    "help": give_help_menu_menu,
    "exit": exit_program_menu
}
