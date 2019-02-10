import time
import os
from time_lib import MyTimeMode
from time_lib import MyTime


class PingResultError(Exception):
    def __init__(self, ping_result_value):
        self.ping_result_value = ping_result_value
        self.message = "Unexpected ping result code was received"


def ping(ip, pinginterval=3):
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


def write_ping_result_to_file(pingresult, ip):
    '''Is used to write ping results to file, return path to the file'''
    currentDirectory = os.getcwd()
    folderToSavePingResultsUpper = ip
    folderToSavePingResultsMiddle = "MONTH_" + str(time.localtime().tm_mon).rjust(2, '0')
    folderToSavePingResultsLower = ip + str(MyTime(MyTimeMode.short))
    folderToSavePingResults = os.path.join(currentDirectory,
                                           folderToSavePingResultsUpper,
                                           folderToSavePingResultsMiddle,
                                           folderToSavePingResultsLower)
    if not os.path.exists(folderToSavePingResults):  # if the path do not exist then
        os.makedirs(folderToSavePingResults)  # create it now!
    with open(os.path.join(folderToSavePingResults,
                           f"ping_{str(MyTime(MyTimeMode.middle))}_{ip}.txt"), mode="a") as f:
        if pingresult == (1, 0):
            f.write(
                f"The remote destination {ip} is reachable, everyting is OKAY.{str(MyTime(MyTimeMode.full))} \n")
        elif pingresult == (0, 1):
            f.write(f"Ping {ip} failed! {str(MyTime(MyTimeMode.full))} \n")
        elif pingresult == None:
            pass
        else:
            raise PingResultError(pingresult)
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
