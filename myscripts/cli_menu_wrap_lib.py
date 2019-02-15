from myscripts import cli_menu


def add_ip_to_monitoring_menu(popen_list: dict, command: list) -> None:
    if len(command) == 3:
        if cli_menu.is_ip_address(command[1]) and cli_menu.is_digit(command[2]):
            cli_menu.add_ip_to_monitoring(command[1], command[2], popen_list)
    else:
        print("You should put ip address after word add then interval in seconds.")
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
        if len(ipexportlist) > 0 and (ipexportlist != "FileError"):
            for ip in ipexportlist:
                x = ip.split('INTERVAL')
                cli_menu.add_ip_to_monitoring(x[0], x[1], popen_list)
        elif ipexportlist == "FileError":
            pass
        else:
            print("File IPLIST.py contains no IPs, nothing will be added to monitoring.")
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