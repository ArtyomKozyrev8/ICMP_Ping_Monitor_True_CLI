import subprocess
import ipaddress
import time
import sys
import re
import os

from myscripts import iplist_file_op


def give_help_menu():
    print()
    print("The following list of commands is available in this program version:\n")
    print("setup:  Print setup and press Enter to make initial setup.")
    print("        IF YOU USE THE PROGRAM FIRST TIME DO setup command!\n")
    print("recipients:  Print recipients and press Enter to create recipients list.")
    print("        IF YOU USE THE PROGRAM FIRST TIME DO recipients command!\n")
    print("add:    Print add and press Enter to add ip to monitoring.")
    print("        Pings are made within certain interval.")
    print("        Example: add 1.1.1.1 10")
    print("        Example: add address interval_in_seconds\n")
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
    print("  IF YOU USE THE PROGRAM FIRST TIME DO setup and recipients commands! ")
    print()


def is_ip_address(ip: str) -> bool:

    try:
        ipaddress.IPv4Address(address=str(ip))
    except ipaddress.AddressValueError:
        print(f"IP {ip} is an incorrect address. It can't be added to monitoring.\n")
        return False
    else:
        return True


def is_digit(interval: str) -> bool:
    try:
        int(interval)
    except ValueError:
        print(f"IP {interval} is not correct time interval in seconds.\nIt can't be added to monitoring.\n")
        return False
    else:
        return True


def analyze_command(command: str) -> list:
    ''' This function is used to analyze CLI command, it removes spaces from command,
        if nothing was printed, you will receive string FreeSpace
        CLI Command can't have more then two words,
        otherwise it is considered as incorrect  and the method return list none '''

    if command.strip() == "":
        command = "FreeSpace"
    command = command.split(" ")
    copied_command = command.copy()
    for element in command:
        if element == "":
            copied_command.remove(element)
    command = copied_command
    if len(command) > 3 or len(command) == 0: # seconds part!!!!
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
        ip_list_in_file = iplist_file_op.read_ip_from_file()[1]
        for ip in ip_in_monitoring_dict.keys():
            for element in ip_list_in_file:
                if re.search(string=element, pattern=ip) is not None:
                    print(" ".join(element.split("INTERVAL")))
                    break
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


def add_ip_to_monitoring(ip: str, interval: int, ip_in_monitoring_dict: dict) -> None:
    if is_ip_address(ip):
        if not is_ip_already_in_monitoring(ip, ip_in_monitoring_dict):
            if sys.platform == 'win32':
                ip_in_monitoring_dict[ip] = subprocess.Popen(["python", "pingsubprocess.py", ip, interval],
                                                             stdout=subprocess.DEVNULL)
            elif sys.platform == 'linux':
                ip_in_monitoring_dict[ip] = subprocess.Popen(["python3", "pingsubprocess.py", ip, interval],
                                                             stdout=subprocess.DEVNULL)
            else:
                print(f"The program is not designed to work in your OS {sys.platform}")
                print("The program will be terminated in 5 seconds, Sorry...")
                time.sleep(5)
                print("Bye")
                time.sleep(1)
                sys.exit()

            print(f"{ip} was added to monitoring\n")
            iplist_file_op.write_ip_to_file(f"{ip}INTERVAL{interval}")  #!!!!


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
            ip_list = iplist_file_op.remove_ip_from_file(ip, ip_list)
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
    return ip_list


def setup():
    print("Please note if you made a mistake, you need to repeat setup process!")
    print('Please give your email box, you gonna send mails from.\nExample: sendmailsfrom@gmail.com')
    while True:
        sender_email = input("Print here: ").strip()
        if  sender_email != "":
            break
        else:
            print("Your email box can't be empty value. Try again")
    print('Please give your mail box password.\nExample: yourpassword')
    while True:
        email_sender_password = input("Print here: ").strip()
        if email_sender_password != "":
            break
        else:
            print("Your mail box can't be empty value. Try again")
    print('Please give your mail server address.\nExample: smtp.gmail.com')
    while True:
        smtp_settings = input("Print here: ").strip()
        if smtp_settings != "":
            break
        else:
            print("Mail server address can't be empty value. Try again")
    print('Please give SMTP server port.\nExample: 587')
    while True:
        smtp_port = input("Print here: ").strip()
        if smtp_port != "":
            try:
                smtp_port = int(smtp_port)
                break
            except:
                print('SMTP server port should be integer value. Try again')
        else:
            print("SMTP server port address can't be empty value. Try again")
    print('Please choose Log Mode. Choose only short or long.')
    while True:
        log_mode = input("Print here: ").strip()
        if log_mode == "short" or log_mode == "long":
            break
        else:
            print("Incorrect Log Mode. Choose only short or long. Try again")

    settings = (sender_email, email_sender_password, smtp_settings, str(smtp_port), log_mode)
    print("You made the following settings:")
    print(f" sender email: {sender_email}\n", f"sender email password: {email_sender_password}\n",
          f"SMTP server address: {smtp_settings}\n", f"SMTP port number: {smtp_port}\n",
          f"Log Mode: {log_mode}\n")
    print("If you made something wrong, repeat setup!")
    way = os.path.join(os.getcwd(), "settings")
    if not os.path.exists(way):
        os.makedirs(way)
    with open(file=os.path.join(way, "settings.py"), mode="w") as f:
        for i in settings:
            f.write(f"{i}\n")


def make_email_recipient_list():
    email_recipients = []
    add_recipient = True
    while add_recipient:
        print("Please enter emails of recipient you would like to notify")
        email = input("Print here: ").strip()
        if len(email.split()) == 1:
            email_recipients.append(email)
            print("Do you want to add another recipient?")
            while True:
                want_to_continue = input("If yes print yes, otherwise press enter: ").strip()
                if want_to_continue.upper() == "YES":
                    break
                elif want_to_continue.upper() == "":
                    add_recipient = False
                    break
                else:
                    print("Incorrect input, please try again.")
        else:
            print("You put incorrect email, please try again!")
    print(f"As a result you have the following list of recipients:\n{email_recipients}")
    way = os.path.join(os.getcwd(), "settings")
    if not os.path.exists(way):
        os.makedirs(way)
    with open(file=os.path.join(way, "email_recipient_list.py"), mode="w") as f:
        for i in email_recipients:
            f.write(f"{i}\n")







