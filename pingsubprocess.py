import threading
import sys
import os
from myscripts import mail_activity, ping_op
from myscripts.time_lib import MyTime


def upload_error_notification_msg():
    file_name = os.path.join(os.getcwd(), "notification_texts", "error_notification.txt")
    try:
        with open(file=file_name, mode='r') as f:
            temporary = f.read()
            return temporary
    except FileNotFoundError:
        sys.stderr.write("The file error_notification.txt does not exist or corrupted. Create the file.\n\n")
        sys.stderr.flush()
        return None


def upload_recovery_notification_msg():
    file_name = os.path.join(os.getcwd(), "notification_texts", "recovery_notification.txt")
    try:
        with open(file=file_name, mode='r') as f:
            temporary = f.read()
            return temporary
    except FileNotFoundError:
        sys.stderr.write("The file recovery_notification.txt does not exist or corrupted. Create the file.\n\n")
        sys.stderr.flush()
        return None


def upload_smtp_settings():
    settings = []
    file_name = os.path.join(os.getcwd(), "settings", "settings.py")
    try:
        with open(file=file_name , mode="r") as f:
            for i in f:
                settings.append(i.strip("\\\n"))
    except FileNotFoundError:
        sys.stderr.write("Settings file does not exist or corrupted.\n\n")
        sys.stderr.write("Delete the file if it exists and do setup command\n\n")
        sys.stderr.write("{} session crushed.\n\n".format(ip))
        sys.stderr.write("To restore session to the ip, add it again!\n")
        sys.stderr.flush()
        sys.exit()
    return settings


def upload_recipients_list():
    recipients = []
    file_name = os.path.join(os.getcwd(), "settings", "email_recipient_list.py")
    try:
        with open(file=file_name, mode="r") as f:
            for i in f:
                recipients.append(i.strip("\\\n"))
    except FileNotFoundError:
        sys.stderr.write("email_recipient_list.py file does not exist or corrupted.\n\n")
        sys.stderr.write("Delete the file if it exists and do recipients command\n\n")
        sys.stderr.write("{} session crushed.\n\n".format(ip))
        sys.stderr.write("To restore session to the ip, add it again!\n")
        sys.stderr.flush()
        sys.exit()
    return recipients


def notificator(pingFailedLetterWasSent, negativePingsInRow, positivePingsInRow,
                email_sender_box, email_recepient_list, error_mail_message, recovery_mail_message,
                email_sender_password, smtp_settings, smtp_port, mode):

    if negativePingsInRow == 4 and not pingFailedLetterWasSent:
        pingFailedLetterWasSent = True
        sys.stderr.write("{} is not reachable.\n\n".format(ip))
        sys.stderr.flush()

        if mode == "short":
            ping_op.write_ping_result_to_file_short_version(pingFailedLetterWasSent, ip)

        negativeLetterThread = threading.Thread(target=mail_activity.send_negative_mail,
                                                args=("{}".format(ip), email_sender_box,
                                                      email_recepient_list,
                                                      error_mail_message,
                                                      email_sender_password,
                                                      smtp_settings,
                                                      smtp_port
                                                      ), )
        negativeLetterThread.start()
        negativeLetterThread.join()

    if positivePingsInRow == 10 and pingFailedLetterWasSent:
        pingFailedLetterWasSent = False
        sys.stderr.write("{} is  reachable again now.\n\n".format(ip))
        sys.stderr.flush()

        if mode == "short":
            ping_op.write_ping_result_to_file_short_version(pingFailedLetterWasSent, ip)

        positiveLetterThread = threading.Thread(target=mail_activity.send_positive_mail,
                                                args=("{}".format(ip), email_sender_box,
                                                      email_recepient_list,
                                                      recovery_mail_message,
                                                      email_sender_password,
                                                      smtp_settings,
                                                      smtp_port
                                                      ), )
        positiveLetterThread.start()
        positiveLetterThread.join()
    return pingFailedLetterWasSent


def main(ip, interval):
    error_mail_message = upload_error_notification_msg()
    recovery_mail_message = upload_recovery_notification_msg()
    if error_mail_message is None or recovery_mail_message is None:
        sys.stderr.write("{} session crushed.\n".format(ip))
        sys.stderr.flush()
        sys.exit()

    settings = upload_smtp_settings()

    email_recepient_list = upload_recipients_list()

    email_sender_box = settings[0]
    email_sender_password = settings[1]
    smtp_settings = settings[2]
    smtp_port = settings[3]
    log_mode = settings[4]

    pingFailedLetterWasSent = False
    positivePingsInRow = 0
    negativePingsInRow = 0
    if log_mode == "long":
        positivePingsThisHourCounterC = 0
        negativePingsThisHourCounterC = 0
        lastAttemptTime = MyTime()
        previousFilePath = ping_op.write_ping_result_to_file(ip=ip, pingresult=None)
    while True:
        if not pingFailedLetterWasSent:
            pingResult = ping_op.ping(ip, interval)
        else:
            pingResult = ping_op.ping(ip, 2)
        if log_mode == "long":
            CurrentFilePath = ping_op.write_ping_result_to_file(pingResult, ip)
            currentTime = MyTime()

            if currentTime.compare_dates(lastAttemptTime):
                ping_op.write_ping_stats_to_file(ip, positivePingsThisHourCounterC,
                                                 negativePingsThisHourCounterC, previousFilePath)
                previousFilePath = CurrentFilePath
                lastAttemptTime = currentTime
                positivePingsThisHourCounterC = 0
                negativePingsThisHourCounterC = 0

            positivePingsThisHourCounterC = positivePingsThisHourCounterC + pingResult[0]
            negativePingsThisHourCounterC = negativePingsThisHourCounterC + pingResult[1]

        if positivePingsInRow < positivePingsInRow + pingResult[0]:
            positivePingsInRow = positivePingsInRow + pingResult[0]
            negativePingsInRow = 0
        if negativePingsInRow < negativePingsInRow + pingResult[1]:
            positivePingsInRow = 0
            negativePingsInRow = negativePingsInRow + pingResult[1]

        pingFailedLetterWasSent = notificator(pingFailedLetterWasSent, negativePingsInRow, positivePingsInRow,
                                              email_sender_box, email_recepient_list, error_mail_message,
                                              recovery_mail_message, email_sender_password, smtp_settings,
                                                   smtp_port, log_mode)


if __name__ == '__main__':
    ip = str(sys.argv[1])
    interval = int(sys.argv[2])
    main(ip, interval)


