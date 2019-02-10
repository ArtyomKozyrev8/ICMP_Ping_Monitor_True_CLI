import time
import os
from time_lib import MyTimeMode
from time_lib import MyTime
import sys


class PingResultError(Exception):
    def __init__(self, ping_result_value):
        self.ping_result_value = f"Unexpected ping result code was received: {ping_result_value}"


def ping(ip, pinginterval=3):
    try:
        if sys.platform == 'win32':
            pingresult = os.system(f"ping -n 1 {ip}")
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
            pingresult = os.system(f"ping -c 1 {ip}")
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
            sys.stderr.write(f"The program is not designed to work in your OS {sys.platform}")
            sys.stderr.write(f"{ip} session crushed.")
            sys.stderr.flush()
            sys.exit()
    except PingResultError as ex:
        sys.stderr.write(f"{ex.ping_result_value}\n\n")
        sys.stderr.write(f"{ip} session crushed.")
        sys.stderr.flush()
        sys.exit()


def write_ping_result_to_file(pingresult, ip):
    '''Is used to write ping results to file, return path to the file'''
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
                           f"ping_{str(MyTime(MyTimeMode.middle))}_{ip}.txt"), mode="a") as f:
        try:
            if pingresult == (1, 0):
                f.write(
                    f"The remote destination {ip} is reachable, everyting is OKAY.{str(MyTime(MyTimeMode.full))} \n")
            elif pingresult == (0, 1):
                f.write(f"Ping {ip} failed! {str(MyTime(MyTimeMode.full))} \n")
            elif pingresult == None: # it is so to allow first ping, see pingsubprocess.py file to understand
                pass
            else:
                raise PingResultError(pingresult)
        except PingResultError as ex:
            sys.stderr.write(f"{ex.ping_result_value}\n\n")
            sys.stderr.write(f"{ip} session crushed.")
            sys.stderr.flush()
            sys.exit()
    FilePath = os.path.join(folderToSavePingResults, f"ping_{str(MyTime(MyTimeMode.middle))}_{ip}.txt")
    return FilePath


def write_ping_stats_to_file(ip, positivePingsThisHourCounter,
                             negativePingsThisHourCounter, previousFilePath):
    '''Writes percent of successfull attempts to file which was used to write ping reuslts in wuthin previous hour'''
    if (positivePingsThisHourCounter + negativePingsThisHourCounter) != 0:
        with open(previousFilePath, mode="a") as f:
            k = 100 * positivePingsThisHourCounter / (positivePingsThisHourCounter + negativePingsThisHourCounter)
            f.write("\n")
            f.write(f"{ip}__positivePingAttempts_Number_is__{positivePingsThisHourCounter}\n")
            f.write(f"{ip}__negativePingAttempts_Number_is__{negativePingsThisHourCounter}\n")
            f.write(f"{ip}__Percent of_positivePingAttempts__is__{k}\n")
            f.write("\n")
