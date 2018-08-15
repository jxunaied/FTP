import ftplib
from io import StringIO
import math

global totalSize

def ftp_connect():
    while True:
        site_address = input('Please enter FTP address: ')
        try:
            with ftplib.FTP(site_address) as ftp:
                ftp.login('SMartBird','12345')
                print(ftp.getwelcome())
                print('Current Directory', ftp.pwd())
                ftp.dir()
                print('Valid commands are cd/get/ls/exit - ex: get readme.txt')
                ftp_command(ftp)
                break  # once ftp_command() exits, end this function (exit program)
        except ftplib.all_errors as e:
            print('Failed to connect, check your address and credentials.', e)

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])
    


def ftp_command(ftp):
    while True:  # Run until 'exit' command is received from user
        command = input('Enter a command: ')
        commands = command.split()  # split command and file/directory into list

        if commands[0] == 'cd': # Change directory
            try:
                ftp.cwd(commands[1])
                print('Directory of', ftp.pwd())
                ftp.dir()
                print('Current Directory', ftp.pwd())
            except ftplib.error_perm as e:  # Handle 550 (not found / no permission error)
                error_code = str(e).split(None, 1)
                if error_code[0] == '550':
                    print(error_code[1], 'Directory may not exist or you may not have permission to view it.')
        elif commands[0] == 'get':  # Download file
            try:
                
                ftp.retrbinary('RETR ' + commands[1], open(commands[1], 'wb').write)
                print('File successfully downloaded.')
                
            except ftplib.error_perm as e:  # Handle 550 (not found / no permission error)
                error_code = str(e).split(None, 1)
                if error_code[0] == '550':
                    print(error_code[1], 'File may not exist or you may not have permission to view it.')
        elif commands[0] == 'ls':  # Print directory listing
            print('Directory of', ftp.pwd())
            ftp.dir()
        elif commands[0] == '..':
            ftp.cwd("../")
            print('Directory of', ftp.pwd())
            ftp.dir()
        elif commands[0] == 'up':
            try:
                file=commands[1]
                print(file)
                myfile = open('/Users/Asus/Desktop/FTP/New folder/New folder (2)/'+ commands[1],'rb')
                ftp.storbinary("STOR " + commands[1],myfile)
                print('File successfully Uploded.')
            except ftplib.error_perm as e:  # Handle 550 (not found / no permission error)
                print('File may not exist or you may not have permission to view it.')
        elif commands[0] == 'rename':
            try: 
               newname = input('Enter New Name: ')
               ftp.rename(commands[1],newname)
               print('\nSuccessfully Rename File: '+ commands[1])
               print('New Name is: '+ newname +'\n')
            except ftplib.error_perm as e:  # Handle 550 (not found / no permission error)
                error_code = str(e).split(None, 1)
                print('###Someting Wrong###')
        elif commands[0] == 'delete':
            try:
                ftp.delete(commands[1])
                print('\nSuccessfully Deleted: '+ commands[1]  +'\n')
            except ftplib.error_perm as e:  # Handle 550 (not found / no permission error)
                error_code = str(e).split(None, 1)
                print('###Someting Wrong###')
        elif commands[0] == 'mkd':
            try:
                ftp.mkd(commands[1])
                print('\nSuccessfully Created: '+ commands[1]  +'\n')
            except ftplib.error_perm as e:  # Handle 550 (not found / no permission error)
                error_code = str(e).split(None, 1)
                print('###Someting Wrong###')
        elif commands[0] == 'rmd':
            try:
                ftp.rmd(commands[1])
                print('\nSuccessfully Removed: '+ commands[1]  +'\n')
            except ftplib.error_perm as e:  # Handle 550 (not found / no permission error)
                error_code = str(e).split(None, 1)
                print('###Someting Wrong###')
        elif commands[0] == 'size':
            try:
                ftp.sendcmd("TYPE i")
                sz = ftp.size(commands[1])
                
                print('\nFile SIze of '+ commands[1]  +' is: ', convert_size(sz) ,'\n')
            except ftplib.error_perm as e:  # Handle 550 (not found / no permission error)
                error_code = str(e).split(None, 1)
                print('###Someting Wrong###')
        elif commands[0] == 'move':
            try: 
                newnamee = input('Enter new File path ex: dirB/hello.txt : ')
                newname = newnamee+commands[1]
                path = ftp.pwd()+commands[1]
                ftp.rename(path,newname)
                print('\nSuccessfully Move File: '+ commands[1])
                print('New Path is: '+ newname +'\n')
            except ftplib.error_perm as e:  # Handle 550 (not found / no permission error)
                error_code = str(e).split(None, 1)
                print('###Someting Wrong###')
        elif commands[0] == 'exit':  # Exit application
            ftp.quit()
            print('Goodbye!')
            break
        else:
            print('Invalid command, try again (valid options: cd/get/ls/exit).')

print('Welcome to Python FTP')
ftp_connect()
