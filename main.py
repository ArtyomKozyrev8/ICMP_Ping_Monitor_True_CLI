import cli_menu
import time
from cli_menu_wrap_lib import menu_wrapper
import sys

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


if __name__ == '__main__':
    if sys.platform == 'win32' or sys.platform == 'linux':
        main()
    else:
        print(f"The program is not designed to work in your OS {sys.platform}")
        print("The program will be terminated in 5 seconds, Sorry...")
        time.sleep(5)
        print("Bye")
        time.sleep(1)
        sys.exit()
