import sqlite3
import os
import time
import sys
import ipaddress


class IpSession:
    def __init__(self, ip, interval, hostname=""):
        ipaddress.IPv4Address(ip) # can raise AddressValueError
        int(interval) # can raise ValueError
        self.ip = ip
        self.interval = interval
        self.hostname = hostname


way = os.path.join(os.getcwd(), "database")
if not os.path.exists(way):
    os.makedirs(way)

dbname = os.path.join(way, 'ipsessions.db')
dbschema = os.path.join(way, 'ipsessions_scheme.sql')


def update_line_into_ipsessions_table(ip_session, db_name=dbname):
    data_to_update = (ip_session.ip, ip_session.interval, ip_session.hostname, ip_session.ip,)
    with sqlite3.connect(db_name) as conn:
        curs = conn.cursor()
        curs.execute('''
        UPDATE ipsessions
        SET ip = ?, interval = ?, hostname = ? 
        WHERE ip = ? ;''', data_to_update)
    print("Information regarding {} was updated".format(ip_session.ip))


def insert_line_into_ipsessions_table(ip_session, db_name=dbname, db_schema=dbschema):
    do_database_exist = not os.path.exists(db_name)
    if not os.path.exists(db_schema):
        print("Database scheme file ipsessions_scheme.sql does not exist.")
        print("The program will be terminated it 5 seconds")
        time.sleep(5)
        sys.exit()
    if do_database_exist:
        with sqlite3.connect(db_name) as conn:
            with open(db_schema, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)
        print("Database ipsessions.db was created!")

    data_to_insert = (ip_session.ip, ip_session.interval, ip_session.hostname)
    try:
        with sqlite3.connect(db_name) as conn:
            curs = conn.cursor()
            curs.execute('''
            INSERT INTO ipsessions (ip, interval, hostname)
            VALUES (?, ?, ?)''', data_to_insert)
        print("Information regarding ip address {} was added to database".format(ip_session.ip))
    except sqlite3.IntegrityError:
        update_line_into_ipsessions_table(ip_session, db_name)


def show_lines_into_ipsessions_table(db_name=dbname):
    with sqlite3.connect(db_name) as conn:
        curs = conn.cursor()
        curs.execute('''SELECT * FROM ipsessions''')
        print("The following sessions are in database now:")
        iplist = []
        for line in curs.fetchall():
            ip, interval, hostname = line
            print("{} {} {}".format(ip, interval, hostname))
            iplist.append(ip)
        return iplist


def extract_ips_from_ipsessions_table(db_name=dbname):
    with sqlite3.connect(db_name) as conn:
        curs = conn.cursor()
        curs.execute('''SELECT * FROM ipsessions''')
        iplist = []
        for line in curs.fetchall():
            ip, interval, hostname = line
            iplist.append(ip)
        return iplist


def del_line_from_ipsessions_table(ip, iplist, db_name=dbname):
    if len(iplist) == 0:
        print("The database is empty, nothing more can be removed.")
    else:
        if ip in iplist:
            data_to_remove = (ip,)
            with sqlite3.connect(db_name) as conn:
                curs = conn.cursor()
                curs.execute('''
                DELETE FROM ipsessions WHERE ip = ?
                ''', data_to_remove)
            print("The ip address {} was removed from database\n".format(ip))
        else:
            print("The ip address {} is not in  database\n".format(ip))


def extract_parameters_of_ip_session_ipsessions_table(ip, db_name=dbname):
    with sqlite3.connect(db_name) as conn:
        data_to_extract = (ip,)
        curs = conn.cursor()
        curs.execute('''SELECT * FROM ipsessions WHERE ip = ?''', data_to_extract)
        line = curs.fetchone()
    return line




'''
x1 = IpSession('1.1.1.1', '100', 'host101')
x2 = IpSession('200.200.1.1', '10', 'host22')
x3 = IpSession('220.220.1.2', '14', 'host52')
x4 = IpSession('101.108.8.9', '14', 'host51')

insert_line_into_ipsessions_table(x1)
insert_line_into_ipsessions_table(x2)
insert_line_into_ipsessions_table(x3)
insert_line_into_ipsessions_table(x4)
print("________________")
print(show_lines_into_ipsessions_table())
print("________________")

iplist = show_lines_into_ipsessions_table()
del_line_from_ipsessions_table('1.1.1.99', iplist)
iplist = show_lines_into_ipsessions_table()
del_line_from_ipsessions_table('1.1.1.1', iplist)
iplist = show_lines_into_ipsessions_table()
del_line_from_ipsessions_table('200.200.1.1', iplist)
iplist = show_lines_into_ipsessions_table()
del_line_from_ipsessions_table('220.220.1.2', iplist)
iplist = show_lines_into_ipsessions_table()
del_line_from_ipsessions_table('101.108.8.9', iplist)
iplist = show_lines_into_ipsessions_table()
del_line_from_ipsessions_table('101.108.8.66', iplist)

print(extract_parameters_of_ip_session_ipsessions_table('1.1.1.99'))
'''