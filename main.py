import cli_menu
import time
from cli_menu_wrap_lib import menu_wrapper

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
    #try:
    main()
    #except Exception as ex:
        #print(f"The following error took place {ex}")
        #time.sleep(30)
