import cli_menu
import time

def main():
    popenList = {} # list of popen subprocess
    cli_menu.hello_banner()
    while True:
        command = input("CLI>: ")
        command = cli_menu.analyze_command(command)
        if command[0] == "add":
            if len(command) > 1:
                if cli_menu.is_ip_address(command[1]):
                    cli_menu.add_ip_to_monitoring(command[1], popenList)
            else:
                print("You should put ip address after word add.")
                print("Print help and press Enter for more information.\n")
        elif command[0] == "del":
            if len(command) > 1:
                cli_menu.remove_ip_from_monitoring(command[1], popenList)
            else:
                print("You should put ip address after word del.")
                print("Print help and press Enter for more information.\n")
        elif command[0] == "import" and len(command) < 2:
            ipexportlist = cli_menu.import_ip_from_file()
            if len(ipexportlist) > 0 and (ipexportlist != "FileError"):
                for ip in ipexportlist:
                    if cli_menu.is_ip_address(ip):
                        cli_menu.add_ip_to_monitoring(ip, popenList)
                    else:
                        print(f"{ip} is not a correct ip, it will not be added to monitoring.")
            elif ipexportlist == "FileError":
                pass
            else:
                print("File IPLIST.py contains no IPs, nothing will be added to monitoring.")
        elif command[0] == "show":
            cli_menu.show_ip_in_monitoring(popenList)
        elif command[0] == "help":
            cli_menu.give_help_menu()
        elif command[0] == "exit":
            cli_menu.exit_program(popenList)
        elif command[0] == "FreeSpace":
            print()
        else:
            print("Incorrect command, Please try again.\n")


if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        print(f"The following error took place {ex}")
        time.sleep(30)
