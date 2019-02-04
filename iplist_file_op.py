def write_ip_to_file(ip: str, filename: str = "IPLIST.txt") -> None:
    try:
        with open(filename, mode='a') as f:
            f.write(f"{ip}\n")
    except Exception as ex:
        print(f"The following unexpected event happened {ex}")


def read_ip_from_file(filename: str = "IPLIST.txt") -> tuple:
    ip_list = []
    try:
        with open(filename, mode="r") as f:
            for ip in f:
                ip_list.append(ip.strip())
    except FileNotFoundError:
        print("The file IPLIST.txt is not reachable or corrupted.")
        print("Try to delete IPLIST.txt if it exists.")
        print("Import failed.\n")
        return False, set(ip_list)
    else:
        return True, set(ip_list)


def remove_ip_from_file(ip: str, ip_list: list) -> None:
    if ip in ip_list:
        ip_list.remove(ip)
        print(f"The {ip} was removed from ip list file IPLIST.txt")
    else:
        print(f"The {ip} is not in ip list file IPLIST.txt")


def rewrite_file(iplist:list, file: str = "IPLIST.txt") -> None:
    with open(file, mode='w') as f:
        for ip in set(iplist):
            f.write(f"{ip}\n")


def show_ip_in_file(ip_list: list):
    '''The function used to show ip addressed, which are in unique file IPLIST.txt'''
    print("The following ips are in file IPLIST.txt:\n")
    for ip in set(ip_list):
        print(ip)
    print()
