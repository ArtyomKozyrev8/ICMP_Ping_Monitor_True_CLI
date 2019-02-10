'''This library work with IPLIST.py file, please note that not all method do operations with file itself,
but do some actions with data which were extracted from file earlier'''

def write_ip_to_file(ip: str, filename: str = "IPLIST.py") -> None:
    try:
        with open(filename, mode='a') as f:
            f.write(f"{ip}\n")
    except Exception as ex:
        print(f"The following unexpected event happened {ex}")


def read_ip_from_file(filename: str = "IPLIST.py") -> tuple:
    ip_list = []
    try:
        with open(filename, mode="r") as f:
            for ip in f:
                ip_list.append(ip.strip())
    except FileNotFoundError:
        print("The file IPLIST.py is not reachable or corrupted.")
        print("Try to delete IPLIST.py if it exists.")
        print("Import failed.\n")
        return False, set(ip_list)
    else:
        return True, set(ip_list)


def remove_ip_from_file(ip: str, ip_list: list) -> None:
    if ip in ip_list:
        ip_list.remove(ip)
        print(f"The {ip} was removed from ip list file IPLIST.py")
    else:
        print(f"The {ip} is not in ip list file IPLIST.py")


def rewrite_file(iplist: list, file: str = "IPLIST.py") -> None:
    with open(file, mode='w') as f:
        for ip in set(iplist):
            f.write(f"{ip}\n")


def show_ip_in_file(ip_list: list):
    '''The function used to show ip addressed, which are in unique file IPLIST.py'''
    print("The following unique ips are in file IPLIST.py:\n")
    for ip in set(ip_list):
        print(ip)
    print()
