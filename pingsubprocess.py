# Before start using the program you should setup it for yourself.
# Find all comments which contain Attention word in the pingsubprocess.py file
# Do the needfull steps which are described in the marked comments.
# Please do not use mailboxes, to send notiffication messages from, with two stage authentification.
# It will require additional lines of code.
# If you struggle any difficulties to setup the program for yourself, feel free to apply to kozirev8@gmail.com
# If any other question, feel free to let me know, I'll do my best to help.


import threading
import sys
import time
import os
import smtplib
import enum
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class MyMailActivity:
    '''This class is used to make mail activity for the program'''
    def send_negative_mail(ipAddress, email_sender, email_receiver):
        '''The method sends negative mail if ip is not reachable'''
        ipAddress = str(ipAddress)
        # Attention! write your own mail subject, do not delete words inside brackets str(MyTime(MyTimeMode.full))
        subject = f"MTT Oy error notification L2 {str(MyTime(MyTimeMode.full))}"
        msg = MIMEMultipart() 
        msg['From'] = email_sender
        msg['To'] = ", ".join(email_receiver)
        msg['Subject'] = subject
        # Attention! write your own mail message, do not delete words inside brackets ipAddress and str(MyTime(MyTimeMode.full))
        body = f"""Dear Partner,\n\nWe observe that address {ipAddress} is not reachable within last 30 seconds.
Now {str(MyTime(MyTimeMode.full))}.
        
We ask you to investigate the issue and undertake all necessary steps to solve the problem.
        
Best Regards,\nMTT Oy Network Monitor Robot"""

        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string() 
        try:
            connection = smtplib.SMTP('smtp.gmail.com', 587) # Attention! This should be settings of you smtp server
            connection.starttls()  
            connection.login(email_sender, 'YourPassword')
            # Attention! Put password of your mailbox to send mails about alarms from
            connection.sendmail(email_sender, email_receiver, text)
            connection.quit()
        except:
            with open(file="ErrorLog.txt", mode="a") as f:
                f.write(str(MyTime(MyTimeMode.full)))
                f.write(f"Connection to SMTP server failed. Session with {ipAddress}. \n")        
            
    def send_positive_mail(ipAddress, email_sender, email_receiver):
        '''The method sends positive mail if ip is reachable again'''
        ipAddress = str(ipAddress)
        # Attention! write your own mail subject, do not delete words inside brackets str(MyTime(MyTimeMode.full))
        subject = f"MTT Oy recovery notification L2 {str(MyTime(MyTimeMode.full))}"
        msg = MIMEMultipart() 
        msg['From'] = email_sender
        msg['To'] = ", ".join(email_receiver)
        msg['Subject'] = subject
        # Attention! write your own message, do not delete words inside brackets ipAddress and str(MyTime(MyTimeMode.full))
        body = f"""Dear Partner,\n\nWe observe that address {ipAddress} has recovered and is stable within last 60 seconds.
Now {str(MyTime(MyTimeMode.full))}.
        
We ask you to investigate and provide us RFO.
        
Best Regards,\nMTT Oy Network Monitor Robot"""

        msg.attach(MIMEText(body, 'plain'))
        text = msg.as_string()  
        try:
            connection = smtplib.SMTP('smtp.gmail.com', 587) # Attention! This should be settings of you smtp server
            connection.starttls()  
            connection.login(email_sender, 'YourPassword') 
            # Attention! Put password of your mailbox to send mails about alarms from
            connection.sendmail(email_sender, email_receiver, text)
            connection.quit()
        except:
            with open(file="ErrorLog.txt", mode="a") as f:
                f.write(str(MyTime(MyTimeMode.full)))
                f.write(f"Connection to SMTP server failed. Session with {ipAddress}. \n")  

class MyTimeMode(enum.Enum):
    '''This class is createc to be used in instances of MyTime class to determine options of __str__ format for that clls'''
    full = "Date: {2}.{1}.{0} Time UTC+3 {3}:{4}:{5}"
    middle = "date{2}_{1}_{0}_timeUTC3_{3}"
    short = "date{2}_{1}_{0}"

class MyTime:
    '''This class is used to display datetiem in the program'''
    def __init__(self,mode=MyTimeMode.middle):
        ''' Is used to create class instance'''
        self.timeNow = time.localtime()
        self.mode = mode

    def __str__(self):
        '''Is used to create string representation of the MyTime Class to be used in print, etc'''
        currentTime = map(lambda x: "0"+str(x) if x<10 else str(x),[self.timeNow.tm_mday,
                                                                  self.timeNow.tm_mon,
                                                                  self.timeNow.tm_year,
                                                                  self.timeNow.tm_hour,
                                                                  self.timeNow.tm_min,
                                                                  self.timeNow.tm_sec])

        return self.mode.value.format(*currentTime) # value is an attribute of enum class
    def compare_dates(self, date_compare):
        '''The class is used to compare instance of MyTime Class'''
        if self.timeNow.tm_year > date_compare.timeNow.tm_year:
            return True
        elif self.timeNow.tm_year < date_compare.timeNow.tm_year:
            return False
        else:
            if self.timeNow.tm_mon > date_compare.timeNow.tm_mon:
                return True
            elif self.timeNow.tm_mon < date_compare.timeNow.tm_mon:
                return False
            else:
                if self.timeNow.tm_mday > date_compare.timeNow.tm_mday:
                    return True
                elif self.timeNow.tm_mday < date_compare.timeNow.tm_mday:
                    return False
                else:
                    if self.timeNow.tm_hour > date_compare.timeNow.tm_hour:
                        return True
                    else:
                        return False
                        
                        

class MyPing():
    def ping(ip, pinginterval=3):
        ''' Is used to do one ping and retrun reults'''
        pingresult = os.system(f"ping -n 1 {ip}")
        if pingresult == 0:
            time.sleep(pinginterval)
            pingresult = (1,0) # successfull attempt
            return pingresult
        elif pingresult == 1:
            pingresult = (0,1) # failed attempt
            return pingresult
        else:
            raise PingResultError
    def write_ping_result_to_file(pingresult, ip):
        '''Is used to wirte ping reults to file, return path to the file'''
        currentDirectory = os.getcwd()
        folderToSavePingResultsUpper = ip
        folderToSavePingResultsLower = ip+str(MyTime(MyTimeMode.short))
        folderToSavePingResults = os.path.join(currentDirectory,folderToSavePingResultsUpper, folderToSavePingResultsLower)
        if not os.path.exists(folderToSavePingResults): # if the path do not exist then 
            os.makedirs(folderToSavePingResults) # create it now!         
        with open(os.path.join(folderToSavePingResults,
                               f"ping_{str(MyTime(MyTimeMode.middle))}_{ip}.txt"),mode="a") as f:
            if pingresult == (1,0):
                f.write(f"The remote destination {ip} is reachable, everyting is OKAY.{str(MyTime(MyTimeMode.full))} \n")
            elif pingresult == (0,1):
                f.write(f"Ping {ip} failed! {str(MyTime(MyTimeMode.full))} \n")
            elif pingresult == None:
                pass
            else:
                raise PingResultError
            FilePath = os.path.join(folderToSavePingResults,f"ping_{str(MyTime(MyTimeMode.middle))}_{ip}.txt")
            return FilePath
                
    def write_ping_stats_to_file(ip, positivePingsThisHourCounter, negativePingsThisHourCounter, previousFilePath):
        '''Writes percent of successfull attempts to file which was used to write ping reuslts in wuthin previous hour'''
        with open(previousFilePath, mode="a") as f:
            k=100*positivePingsThisHourCounter/(positivePingsThisHourCounter+negativePingsThisHourCounter)
            f.write("\n")
            f.write(f"{ip}__positivePingAttempts_Number_is__{positivePingsThisHourCounter}\n")
            f.write(f"{ip}__negativePingAttempts_Number_is__{negativePingsThisHourCounter}\n")
            f.write(f"{ip}__Percent of_positivePingAttempts__is__{k}\n")
            f.write("\n")
                    
def main(ip):
    pingFailedLetterWasSent = False
    positivePingsThisHourCounterC = 0
    negativePingsThisHourCounterC = 0
    positivePingsInRow = 0
    negativePingsInRow = 0
    lastAttemptTime = MyTime()
    previousFilePath = MyPing.write_ping_result_to_file(ip=ip,pingresult=None)
    while(True):
        pingResult = MyPing.ping(ip)
        CurrentFilePath = MyPing.write_ping_result_to_file(pingResult, ip)
        currentTime = MyTime()
        
        if currentTime.compare_dates(lastAttemptTime):
            MyPing.write_ping_stats_to_file(ip, positivePingsThisHourCounter=positivePingsThisHourCounterC,
                                            negativePingsThisHourCounter=negativePingsThisHourCounterC,
                                            previousFilePath=previousFilePath)
            previousFilePath = CurrentFilePath
            lastAttemptTime = currentTime
            positivePingsThisHourCounterC = 0
            negativePingsThisHourCounterC = 0
            
        positivePingsThisHourCounterC = positivePingsThisHourCounterC+pingResult[0]
        negativePingsThisHourCounterC = negativePingsThisHourCounterC+pingResult[1]
        
        if positivePingsInRow < positivePingsInRow+pingResult[0]:
            positivePingsInRow = positivePingsInRow+pingResult[0]
            negativePingsInRow = 0
        if negativePingsInRow < negativePingsInRow+pingResult[1]:
            positivePingsInRow = 0
            negativePingsInRow = negativePingsInRow+pingResult[1]                
        if negativePingsInRow == 4 and pingFailedLetterWasSent == False:
            print("Negative mail was sent")
            pingFailedLetterWasSent = True
            # Attention! Put your own mail settings in the code below, do not remove f{ip}:
            negativeLetterThread = threading.Thread(target=MyMailActivity.send_negative_mail,
                                                    args=(f"{ip}","sendfrom@gmail.com",
                                                                 ["sendto1@gmail.com",
                                                                  "sendto28@gmail.com",
                                                                  "sendto3@gmail.com"],))
            negativeLetterThread.start()
            negativeLetterThread.join()
        if positivePingsInRow == 20 and pingFailedLetterWasSent == True:
            print("Positive mail was sent")
            pingFailedLetterWasSent=False
            # Attention!Put your own mail settings in the code below, do not remove f{ip}:
            positiveLetterThread = threading.Thread(target=MyMailActivity.send_negative_mail,
                                                    args=(f"{ip}","sendfrom@gmail.com",
                                                                 ["sendto1@gmail.com",
                                                                  "sendto28@gmail.com",
                                                                  "sendto3@gmail.com"],))
            positiveLetterThread.start()
            positiveLetterThread.join()

if __name__ == '__main__':
    ip = str(sys.argv[1])
    main(ip)


