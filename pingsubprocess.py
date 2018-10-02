# Before start using the program you should setup it for yourself.
# Find all comments which contain Attention word in the pingsubprocess.py file
# Do the needfull steps which are described in the marked comments.
# Please do not use mailboxes, to send notiffication messages from, with two stage authentification.
# It will require additional lines of code.
# If you struggle any difficulties to setup the program for yourself, feel free to apply to kozirev8@gmail.com
# If any other question, feel free to let me know, I'll do my best to help.

import subprocess
import time
import ipaddress
import sys

class IplistFileOp:
    '''This class was defined to store all operations which could be made with IPLIST.txt
    IPLIST.txt contains list of ip addresses which have ever been used in monitoring'''
    
    __all__ = ["write_ip_to_file", "read_ip_from_file", "remove_ip_from_file", "rewrite_file", "show_ip_in_file"]
    
    def write_ip_to_file(ip, file="IPLIST.txt"):
        ''' Types: ip is a string | file is a .txt file
        Output Types: void
        The method write ip to file to use it in further program Starts
        If user would like to read list of ip which were monitored later'''      
        with open(file, mode='a') as f:
            f.write(f"{ip}\n")
            
    def read_ip_from_file(file="IPLIST.txt"):
        ''' Types: file is a .txt file
        Output Types: tuple Boolean,Set
        The function is used to read Ip addresses from file and return it as a list'''
        ipList = []
        try:
            with open(file, mode = "r") as f:
                for ip in f:
                    ipList.append(ip.strip())
        except FileNotFoundError:
            print("The file IPLIST.txt is not reachable or corrupted.")
            print("Try to delete IPLIST.txt if it exists.")
            print("Import failed.\n")
            return (False, set(ipList))
        else:
            return (True, set(ipList))
        
    def remove_ip_from_file(ip, iplist):
        ''' Types: ip is a string | iplist is a list
        Output Types: void
        The function is used to read Ip addresses from file and return it as a list'''
        if ip in iplist:
            iplist.remove(ip)
            print(f"The {ip} was removed from ip list file IPLIST.txt")
        else: print(f"The {ip} is not in ip list file IPLIST.txt")
            
    def rewrite_file(iplist, file="IPLIST.txt"):
        ''' Types: iplist is a list | file is a .txt file 
        Output Types: void
        The function is used to read ip addresses from file and return it as a list'''
        with open(file, mode = 'w') as f:
            for ip in set(iplist):
                f.write(f"{ip}\n")
            
    def show_ip_in_file(iplist):
        '''Types: iplist is List
        The function used to show ip addressed, which are in unique file IPLIST.txt'''
        print("The following ips are in file IPLIST.txt:\n")
        for ip in set(iplist):
              print(ip)
        print()

class CLI_MENU:
    '''This class contains methods for CLI menu, which is used in the program'''
    
    __all__ = ["is_ip_already_in_monitoring", "stop_popen", "add_ip_to_monitoring",
               "import_ip_from_file", "is_ip_address", "analyze_command", "exit_program",
              "show_ip_in_monitoring", "give_help_menu", "hello_banner"]

    def is_ip_already_in_monitoring(ip, popenlist):
        ''' Input Types: ip is a string |  popenlist is a dictionary |
        Output Types: Boolean
        The method is used to check if ip is already in monitoring,
        to prevent creation of duplicated subpocesses.
        popenlist is  dictionary where key is ip address and 
        value is subprocess.Popen'''

        if ip in popenlist.keys():
            print(f"{ip} address is already in monitoring.\n")
            return True
        else:
            return False
    
    def stop_popen(ip, popenlist):
        ''' Input Types: ip is a string |  popenlist is a dictionary |
        Output Types: void
        The method us used to remove ip from monitoring, if there is no such ip
        we get error message.
        popenlist is  dictionary where key is ip address and 
        value is subprocess.Popen '''
    
        if ip in popenlist.keys():
            popenlist[ip].kill()
            del popenlist[ip]
            print(f"{ip} is removed from monitoring\n")
        else:
            print(f"The mentioned ip {ip} address is not in monitoring.\n")
            print("Use show command to see all ip which are monitored.")
            print("To get help print help then press Enter\n")

    def add_ip_to_monitoring(ip, popenlist):
        ''' Types: ip is a string |  popenlist is a dictionary |
        Output Types: void
        The method us used to add ip in monitoring.
        ip is checked to be correct ip before adding in monitoring,
        see is_ip_already_in_monitoring method
        popenlist is  dictionary where key is ip address and 
        value will be subprocess.Popen'''
        if CLI_MENU.is_ip_address(str(ip)):
            if not CLI_MENU.is_ip_already_in_monitoring(ip,popenlist): 
                popenlist[ip]=subprocess.Popen(["python", "pingsubprocess.py", ip], stdout=subprocess.DEVNULL)
                print(f"{ip} was added to monitoring\n")
                IplistFileOp.write_ip_to_file(ip)
                 
    def import_ip_from_file():
        ''' Types: none
        Outpust Types: ipList - string or set
        This method is used in CLI menu to upload to program list of ip addresses, which have ever been
        used in the program before, the method gives opportunity to delete some ips from file IPLIST.txt
        and only then import the rest ips to monitoring'''
        
        readFromFileResult = IplistFileOp.read_ip_from_file()
        continueImport = readFromFileResult[0]
        ipList = readFromFileResult[1]
        if not continueImport:
            ipList = "FileError"
            return ipList
        while(continueImport):
            IplistFileOp.show_ip_in_file(ipList)
            ip = input("Print ip you would like to remove, otherwise print Enter:\n")
            if ip == "":
                continueImport = False
                break
            else:                
                IplistFileOp.remove_ip_from_file(ip,ipList)
                IplistFileOp.show_ip_in_file(ipList)
            while(True):
                removeMoreIP = input("Print yes and press Enter to remove more ip, otherwise press Enter:\n")
                if removeMoreIP.upper() == "YES":
                    continueImport = True
                    break
                elif removeMoreIP == "":
                    continueImport = False
                    IplistFileOp.rewrite_file(ipList)
                    break
                else:
                    print("Incorrect input was made, please try again.\n")
        return set(ipList)                               
              
    def is_ip_address(ip):
        ''' Types: ip is a string
        Output Types: Boolean
        This function is used to understand if the second part of CLI command is ip
        address. It returns True or False. The function is used to check add |x.x.x.x 
        command|, to be exact metod check the second part of the command x.x.x.x'''
    
        try:
            ipaddress.IPv4Address(address = str(ip))
        except  ipaddress.AddressValueError:
            print(f"IP {ip} is an incorrect address. It can't be added to monitoring.\n")
            return False
        else:
            return True

    def analyze_command(command):
        ''' Types: command is a string from input method
        Output Types: list
        This function is used to analyze CLI command, it removes spaces from command,
        if nothing was printed, the method gives the command incorrect value none to process it
        in main method and cause next error message. CLI Command can't have more then
        two words, otherwise it is considered as incorrect  and the method gives command
        an incorrect value none to cause error in main method''' 
    
        if command == "":
            command = "FreeSpace"
        command = command.split(" ")
        copyCommand = command.copy()
        for element in command:
            if element == "":
                copyCommand.remove(element)
        command = copyCommand
        if len(command) > 2 or len(command)==0:
            command = ["none"]
        return command

    def exit_program(popenlist):
        '''Types: popenlist is a dictionary |
        This method is used to exit from the program, it takes list of ip in monitoring,
        read subprocesses which are active now, if the processess are not stopped,
        the program will not be terminated correctly'''
    
        if len(popenlist):
            for activepopen in popenlist.values():
                activepopen.kill()
        print("The program will be terminated in 5 seconds.\n")
        time.sleep(4)
        print("Bye...\n")
        time.sleep(1)
        sys.exit()
    
    def show_ip_in_monitoring(popenlist):
        '''Types: popenlist is a dictionary |
        This method is used to show what ip are monitored now'''
        if not len(popenlist)==0:
            for ip in popenlist.keys():
                print(f"{ip} is monitored now.")
        else:
            print("There is no ip in monitoring now.\n")
    
    def give_help_menu():
        '''This method is used to show CLI commands which are used in the program'''
        print()
        print("The following list of commands is available in this program version:\n")
        print("add:    Print add and press Enter to add ip to monitoring.")
        print("        Example: add 1.1.1.1 \n")
        print("del:    Print del and press Enter to remove ip from monitoring.")
        print("        Example: del 1.1.1.1 \n")
        print("show:   Print show and press Enter to see what list of ip is monitored.\n")
        print("import: Print read and press Enter to read list of ip from IPLIST.txt file.\n")
        print("exit:   Print exit and press Enter to quit the program.\n")
        print("help:   Print help and press Enter to get help menu.\n")
        print("Just press Enter to get some free space in console screen.\n")
        
    def hello_banner():
        '''This method just print hello banner'''
        print("**********************************************************************")
        print("*                                                                    *")
        print("*         Hello and Welcome to ICMP PING MONITOR TRUE CLI            *")
        print("*                                                                    *")
        print("**********************************************************************")
        print()
        print("   Type your command, if you need help - print help and press Enter   ")
        print()
    
def main():
    popenList = {}
    CLI_MENU.hello_banner()
    while True:
        command = input("CLI>: ")
        command = CLI_MENU.analyze_command(command)
        if command[0] == "add":
            if len(command) > 1:
                if CLI_MENU.is_ip_address(command[1]):
                    CLI_MENU.add_ip_to_monitoring(ip=command[1],popenlist=popenList)
            else:
                print("You should put ip address after word add.")
                print("Print help and press Enter for more information.\n")
        elif command[0] == "del":
            if len(command) > 1:
                CLI_MENU.stop_popen(ip=command[1], popenlist=popenList)
            else:
                print("You should put ip address after word del.")
                print("Print help and press Enter for more information.\n")
        elif command[0] == "import" and len(command) < 2:
            ipexportlist = CLI_MENU.import_ip_from_file()
            if len(ipexportlist) > 0 and (ipexportlist != "FileError"):
                for ip in ipexportlist:
                    if CLI_MENU.is_ip_address(ip):
                        CLI_MENU.add_ip_to_monitoring(ip,popenList)
                    else: print(f"{ip} is not a correct ip, it will not be added to monitoring.")
            elif ipexportlist == "FileError":
                pass
            else: print("File IPLIST.txt contains no IPs, nothing will be added to monitoring.")        
        elif command[0] == "show": CLI_MENU.show_ip_in_monitoring(popenlist=popenList)
        elif command[0] == "help": CLI_MENU.give_help_menu()
        elif command[0] == "exit": CLI_MENU.exit_program(popenlist=popenList)
        elif command[0] == "FreeSpace": print()
        else: print("Incorrect command, Please try again.\n")

if __name__ == '__main__':
    main()
