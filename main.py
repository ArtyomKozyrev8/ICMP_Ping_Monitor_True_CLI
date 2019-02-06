import cli_menu

from cli_menu_wrap_lib import menu_wrapper

def main():
    popenList = {} # list of popen subprocess
    cli_menu.hello_banner()
    while True:
        command = input("CLI>: ")
        command = cli_menu.analyze_command(command)
        if command[0] in menu_wrapper.keys():
            menu_wrapper[command[0]](popenList, command)
        elif command[0] == "FreeSpace":
            print()
        else:
            print("Incorrect command, Please try again.\n")


if __name__ == '__main__':
    main()

