import subprocess
import ipaddress
import time
import sys

import iplist_file_op


def give_help_menu():
    print()
    print("The following list of commands is available in this program version:\n")
    print("add:    Print add and press Enter to add ip to monitoring.")
    print("        Example: add 1.1.1.1 \n")
    print("del:    Print del and press Enter to remove ip from monitoring.")
    print("        Example: del 1.1.1.1 \n")
    print("show:   Print show and press Enter to see what list of ip is monitored.\n")
    print("import: Print read and press Enter to read list of ip from IPLIST.py file.\n")
    print("exit:   Print exit and press Enter to quit the program.\n")
    print("help:   Print help and press Enter to get help menu.\n")
    print("Just press Enter to get some free space in console screen.\n")


def hello_banner():
    print("**********************************************************************")
    print("*                                                                    *")
    print("*         Hello and Welcome to ICMP PING MONITOR TRUE CLI            *")
    print("*                                                                    *")
    print("**********************************************************************")
    print()
    print("   Type your command, if you need help - print help and press Enter   ")
    print()


def is_ip_address(ip: str) -> bool:

    try:
        ipaddress.IPv4Address(address=str(ip))
    except ipaddress.AddressValueError:
        print(f"IP {ip} is an incorrect address. It can't be added to monitoring.\n")
        return False
    else:
        return True


def analyze_command(command: str) -> list:
    ''' This function is used to analyze CLI command, it removes spaces from command,
        if nothing was printed, you will receive string FreeSpace
        CLI Command can't have more then two words,
        otherwise it is considered as incorrect  and the method return
        string none to cause error in main method'''

    if command.strip() == "":
        command = "FreeSpace"
    command = command.split(" ")
    copied_command = command.copy()
    for element in command:
        if element == "":
            copied_command.remove(element)
    command = copied_command
    if len(command) > 2 or len(command) == 0:
        command = ["none"]
    return command


def exit_program(ip_in_monitoring_dict: dict) -> None:
    if len(ip_in_monitoring_dict):
        for active_popen in ip_in_monitoring_dict.values():
            active_popen.kill()
    print("The program will be terminated in 5 seconds.\n")
    time.sleep(4)
    print("Bye...\n")
    time.sleep(1)
    sys.exit()


def show_ip_in_monitoring(ip_in_monitoring_dict: dict) -> None:

    if not len(ip_in_monitoring_dict) == 0:
        for ip in ip_in_monitoring_dict.keys():
            print(f"{ip} is monitored now.")
    else:
        print("There is no ip in monitoring now.\n")


def is_ip_already_in_monitoring(ip: str, ip_in_monitoring_dict: dict) -> bool:
    if ip in ip_in_monitoring_dict.keys():
        print(f"{ip} address is already in monitoring.\n")
        return True
    else:
        return False


def remove_ip_from_monitoring(ip: str, ip_in_monitoring_dict: dict) -> None:

    if ip in ip_in_monitoring_dict.keys():
        ip_in_monitoring_dict[ip].kill()
        del ip_in_monitoring_dict[ip]
        print(f"{ip} is removed from monitoring\n")
    else:
        print(f"The mentioned ip {ip} address is not in monitoring.\n")
        print("Use show command to see all ip which are monitored.")
        print("To get help print help then press Enter\n")


def add_ip_to_monitoring(ip: str, ip_in_monitoring_dict: dict) -> None:
    if is_ip_address(ip):
        if not is_ip_already_in_monitoring(ip, ip_in_monitoring_dict):
            ip_in_monitoring_dict[ip] = subprocess.Popen(["python", "pingsubprocess.py", ip],
                                                         stdout=subprocess.DEVNULL)
            print(f"{ip} was added to monitoring\n")
            iplist_file_op.write_ip_to_file(ip)


def import_ip_from_file() -> set:
    read_from_file_result = iplist_file_op.read_ip_from_file()
    continue_import = read_from_file_result[0]
    ip_list = read_from_file_result[1]
    if not continue_import:
        ip_list = "FileError"
        return ip_list
    while continue_import:
        iplist_file_op.show_ip_in_file(ip_list)
        ip = input("Print ip you would like to remove, otherwise print Enter:\n")
        if ip == "":
            break
        else:
            iplist_file_op.remove_ip_from_file(ip, ip_list)
            iplist_file_op.show_ip_in_file(ip_list)
        while True:
            remove_more_ip = input("Print yes and press Enter to remove more ip, otherwise press Enter:\n")
            if remove_more_ip.upper() == "YES":
                continue_import = True
                break
            elif remove_more_ip == "":
                continue_import = False
                iplist_file_op.rewrite_file(ip_list)
                break
            else:
                print("Incorrect input was made, please try again.\n")
    return set(ip_list)

