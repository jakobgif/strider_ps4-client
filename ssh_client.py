import paramiko
import time

import loginData as login

def ssh_connect():
    print("Trying to connect to Strider")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(login.host, username=login.username, password=login.password)

        if ssh.get_transport().is_active():
            print("Connection successful.")

            # time.sleep(2)

            channel = ssh.invoke_shell()
            output = channel.recv(1000).decode('utf-8')

            #send the command to the CLI
            channel.send('cd Desktop/spider-strider/ && sudo ./Strider.exe\n') #start strider applciation
            output = channel.recv(1000).decode('utf-8')
            time.sleep(2)

            channel.send('-dev\r\n')
            time.sleep(2)
            output = channel.recv(1000).decode('utf-8')
            print(output)

            return ssh, channel  # Return the connection and channel

    except Exception as e:
        print(f"Error: Unable to connect to the server. {e}")
        return None, None

def ssh_close(connection):
    if connection:
        connection.close()
        print("Connection closed.")

def send_command(command, channel):
    if channel:
        channel.send(command + '\r\n')
        # time.sleep(2)
        # output = channel.recv(4096).decode('utf-8')
        # print(output)

