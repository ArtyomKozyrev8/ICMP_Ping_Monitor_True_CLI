'''This library work with IPLIST.py file, please note that not all method do operations with file itself,
but do some actions with data which were extracted from file earlier'''
import re


def write_ip_to_file(ip: str, filename: str = "IPLIST.py") -> None:
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
                f.write(f"{ip}\n")
        except Exception as ex:
            print(f"The following unexpected event happened {ex}")
    else:
        file_text = re.sub(string=file_text, pattern=f"{x}INTERVAL.*", repl=ip)
        try:
            with open(filename, mode='w') as f:
                f.write(file_text)
        except Exception as ex:
            print(f"The following unexpected event happened {ex}")


def read_ip_from_file(filename: str = "IPLIST.py") -> tuple:
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
                print(f"The {ip} was removed from ip list file IPLIST.py")
                break
        ip_list = temp_ip_list
        end = len(ip_list)
        if end == start:
            print(f"The {ip} is not in ip list file IPLIST.py")
    else:
        print(f"The IPLIST.py file is already empty")
    return ip_list


def rewrite_file(iplist: list, file: str = "IPLIST.py") -> None:
    with open(file, mode='w') as f:
        for ip in iplist:
            if ip is not "\n":
                f.write(f"{ip}\n")


def show_ip_in_file(ip_list: list):
    '''The function used to show ip addressed, which are in unique file IPLIST.py'''
    print("The following unique ips are in file IPLIST.py:\n")
    for ip in ip_list:
        address = ip.split("INTERVAL")[0]
        interval = ip.split("INTERVAL")[1]
        print(f"{address} {interval}")
    print()
