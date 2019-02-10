# ICMP_Ping_Monitor_True_CLI
The program is created to ping several ip addresses, put results in separate txt files, distribute files between folders, send email if ip is not reachable, send email if ip is reachable again. All action are independent for each ip address.

The program has TRUE CLI, which is similar to CMD or router CLI. The CLI is based on subprocess.Popen class.

Note that the program can be used only in Windows OS and Unix (tested in Ubuntu 18.04) now, but you can do some changes to try to use it in your OS.

The program need Python3.6 or older.

To use the program you need to upload all .py and txt files  files and put them in one folder. To start program start main.py file. 

Feel free to ask questions and give remommendations. Feel free to use the code in your projects or to to learn from.

If you face any probelms to do it, feel free to apply to me kozirev8@gmail.com , I'll do my best to help.

The program is not the final version, I'm going to add new changes in future, new contributors are welcome.

File list you should have:

cli_menu.py
cli_menu_wrap_lib.py
iplist_file_op.py
mail_activity.py
main.py
ping_op.py
pingsubprocess.py
time.lib.py

recovery_notification.txt
error_notification.txt

All other files to run program will be automatically created after you did all required steps during first launch of the program.

If it is first launch, do setup and recipients commands. Note that when you start the commands you rewrite data, rather than add any new information to the old one.


