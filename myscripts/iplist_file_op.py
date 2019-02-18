'''This library work with IPLIST.py file, please note that not all method do operations with file itself,
but do some actions with data which were extracted from file earlier'''
import re
import os

way = os.path.join(os.getcwd(), "settings")
if not os.path.exists(way):
    os.makedirs(way)
file_name = os.path.join(way, "IPLIST.py")


def write_ip_to_file(ip: str, filename: str = file_name) -> None:
    file_text = ""
    try:
        with open(filename, mode='r') as f:
            file_text = f.read()
    except FileNotFoundError:
        pass
    x = ip.split("INTERVAL")[0]
    if x not in file_text:
        try:
            with open(filename, mode='a') as f:
                f.write("{}\n".format(ip))
        except Exception as ex:
            print("The following unexpected event happened {}".format(ex))
    else:
        file_text = re.sub(string=file_text, pattern="{}INTERVAL.*".format(x), repl=ip)
        try:
            with open(filename, mode='w') as f:
                f.write(file_text)
        except Exception as ex:
            print("The following unexpected event happened {}".format(ex))


def read_ip_from_file(filename: str = file_name) -> tuple:
    ip_list = []
    try:
        with open(filename, mode="r") as f:
            for ip in f:
                if ip is not "\n":
                    ip_list.append(ip.strip('\n')) #!!!!!!!!
    except FileNotFoundError:
        print("The file IPLIST.py is not reachable or corrupted.")
        print("Try to delete IPLIST.py if it exists.")
        print("Import failed.\n")
        return False, ip_list
    else:
        return True, ip_list


def remove_ip_from_file(ip: str, ip_list: list) -> None:
    if len(ip_list) > 0:
        start = len(ip_list)
        temp_ip_list = ip_list.copy()
        for record in ip_list:
            if re.search(string=record, pattern=ip) is not None:
                temp_ip_list.remove(record)
                print("The {} was removed from ip list file IPLIST.py".format(ip))
                break
        ip_list = temp_ip_list
        end = len(ip_list)
        if end == start:
            print("The {} is not in ip list file IPLIST.py".format(ip))
    else:
        print("The IPLIST.py file is already empty")
    return ip_list


def rewrite_file(iplist: list, file: str = file_name) -> None:
    with open(file, mode='w') as f:
        for ip in iplist:
            if ip is not "\n":
                f.write("{}\n".format(ip))


def show_ip_in_file(ip_list: list):
    '''The function used to show ip addressed, which are in unique file IPLIST.py'''
    print("The following unique ips are in file IPLIST.py:\n")
    for ip in ip_list:
        address = ip.split("INTERVAL")[0]
        interval = ip.split("INTERVAL")[1]
        print("{} {}".format(address, interval))
    print()
