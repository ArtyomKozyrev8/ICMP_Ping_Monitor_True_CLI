from myscripts import cli_menu
import time
from myscripts.cli_menu_wrap_lib import menu_wrapper
import sys


def check_if_all_subprocess_alive(popen_list: dict)-> dict:
    if popen_list:
        popen_list_copy = popen_list.copy()
        for ip in popen_list.keys():
            if popen_list[ip].poll() is not None:
                cli_menu.remove_ip_from_monitoring(ip, popen_list_copy)
        popen_list = popen_list_copy
    return popen_list


def main():
    popen_list = {} # dictionary of popen subprocesses
    cli_menu.hello_banner()
    while True:
        command = input("CLI>: ")
        command = cli_menu.analyze_command(command)
        if command[0] in menu_wrapper.keys():
            menu_wrapper[command[0]](popen_list, command)
        elif command[0] == "FreeSpace":
            print()
        else:
            print("Incorrect command, Please try again.\n")
        popen_list = check_if_all_subprocess_alive(popen_list)


if __name__ == '__main__':
    if sys.platform == 'win32' or sys.platform == 'linux':
        main()
    else:
        print("The program is not designed to work in your OS {}".format(sys.platform))
        print("The program will be terminated in 5 seconds, Sorry...")
        time.sleep(5)
        print("Bye")
        time.sleep(1)
        sys.exit()
