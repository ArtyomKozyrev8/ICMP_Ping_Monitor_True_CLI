import time
import os
from myscripts.time_lib import MyTimeMode
from myscripts.time_lib import MyTime
from myscripts import database_op
import sys



class PingResultError(Exception):
    def __init__(self, ping_result_value):
        self.ping_result_value = "Unexpected ping result code was received: {}".format(ping_result_value)


def ping(ip, pinginterval=3):
    pinginterval = int(pinginterval)
    try:
        ipaddress, interval, hostname = database_op.extract_parameters_of_ip_session_ipsessions_table(ip)
        if sys.platform == 'win32':
            pingresult = os.system("ping -n 1 {}".format(ip))
            if pingresult == 0:
                time.sleep(pinginterval)
                pingresult = (1, 0)  # successfull attempt
                return pingresult
            elif pingresult == 1:
                pingresult = (0, 1)  # failed attempt
                return pingresult
            else:
                raise PingResultError(pingresult)
        elif sys.platform == 'linux':
            pingresult = os.system("ping -c 1 {}".format(ip))
            if pingresult == 0:
                time.sleep(pinginterval)
                pingresult = (1, 0)  # successfull attempt
                return pingresult
            elif pingresult == 256:
                pingresult = (0, 1)  # failed attempt
                return pingresult
            else:
                raise PingResultError(pingresult)
        else:

            sys.stderr.write("The program is not designed to work in your OS {}".format(sys.platform))
            sys.stderr.write("{} {} session crushed.".format(ip, hostname))
            sys.stderr.flush()
            sys.exit()
    except PingResultError as ex:
        sys.stderr.write("{}\n\n".format(ex.ping_result_value))
        sys.stderr.write("{} {} session crushed.".format(ip, hostname))
        sys.stderr.flush()
        sys.exit()


def write_ping_result_to_file(pingresult, ip):
    '''Is used to write ping results to file, return path to the file'''
    ipaddress, interval, hostname = database_op.extract_parameters_of_ip_session_ipsessions_table(ip)
    currentDirectory = os.getcwd()
    folderToSavePingResultsUpper = ip
    folderToSavePingResultsMiddle = "Year_" + str(time.localtime().tm_year) + "Month_"\
                                    + str(time.localtime().tm_mon).rjust(2, '0')
    folderToSavePingResultsLower = ip + str(MyTime(MyTimeMode.short))
    folderToSavePingResults = os.path.join(currentDirectory,
                                           folderToSavePingResultsUpper,
                                           folderToSavePingResultsMiddle,
                                           folderToSavePingResultsLower)
    if not os.path.exists(folderToSavePingResults):  # if the path do not exist then
        os.makedirs(folderToSavePingResults)  # create it now!
    with open(os.path.join(folderToSavePingResults,
                           "ping_{}_{}.txt".format(str(MyTime(MyTimeMode.middle)), ip)), mode="a") as f:
        try:
            if pingresult == (1, 0):
                f.write(
                    "The remote destination {} is reachable.{} \n".format(ip, str(MyTime(MyTimeMode.full))))
            elif pingresult == (0, 1):
                f.write("Ping {} failed! {} \n".format(ip, str(MyTime(MyTimeMode.full))))
            elif pingresult is None: # it is so to allow first ping, see pingsubprocess.py file to understand
                pass
            else:
                raise PingResultError(pingresult)
        except PingResultError as ex:
            sys.stderr.write("{}\n\n".format(ex.ping_result_value))
            sys.stderr.write("{} {} session crushed.".format(ip, hostname))
            sys.stderr.flush()
            sys.exit()
    FilePath = os.path.join(folderToSavePingResults, "ping_{}_{}.txt".format(str(MyTime(MyTimeMode.middle)), ip))
    return FilePath


def write_ping_result_to_file_short_version(event, ip):
    folder_to_save_ping_results = os.path.join(os.getcwd(), ip)
    if not os.path.exists(folder_to_save_ping_results):  # if the path do not exist then
        os.makedirs(folder_to_save_ping_results)  # create it now!
    file_name = "Year_" + str(time.localtime().tm_year) + "Month_"\
                                    + str(time.localtime().tm_mon).rjust(2, '0')
    with open(os.path.join(folder_to_save_ping_results, "{}.txt".format(file_name)), mode="a") as f:
        if event:
            f.write("The address {} is not reachable! {} \n".format(ip, str(MyTime(MyTimeMode.full))))
        else:
            f.write("The address {} is reachable again, {} \n".format(ip, str(MyTime(MyTimeMode.full))))


def write_ping_stats_to_file(ip, positivePingsThisHourCounter,
                             negativePingsThisHourCounter, previousFilePath):
    '''Writes percent of successfull attempts to file which was used to write ping reuslts in wuthin previous hour'''
    if (positivePingsThisHourCounter + negativePingsThisHourCounter) != 0:
        with open(previousFilePath, mode="a") as f:
            k = 100 * positivePingsThisHourCounter / (positivePingsThisHourCounter + negativePingsThisHourCounter)
            f.write("\n")
            f.write("{}__positivePingAttempts_Number_is__{}\n".format(ip, positivePingsThisHourCounter))
            f.write("{}__negativePingAttempts_Number_is__{}\n".format(ip, negativePingsThisHourCounter))
            f.write("{}__Percent of_positivePingAttempts__is__{}\n".format(ip, k))
            f.write("\n")
