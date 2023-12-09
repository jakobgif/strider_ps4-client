import paramiko
import time

command = "-av"
host = "192.168.0.81"
username = "student"
password = "student"

def ssh_connect():
    print("Trying to connect to Strider")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, username=username, password=password)

        if ssh.get_transport().is_active():
            print("Connection successful.")

            # time.sleep(2)

            channel = ssh.invoke_shell()
            output = channel.recv(1000).decode('utf-8')

            # Send the command to the CLI
            channel.send('/home/student/EmbSys/build/spider-strider/CLI\n')
            output = channel.recv(1000).decode('utf-8')
            time.sleep(2)

            channel.send('--apiversion\r\n')
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

