#! /usr/bin/env python

'''
Python for Network Engineers week 4 exercise 2:

Use Paramiko to change the 'logging buffered <size>' configuration on 
pynet-rtr2. This will require that you enter into configuration mode.

Stacy Sherman 8/22/16

'''


import paramiko
from getpass import getpass
from time import sleep

ip_addr = '184.105.247.71'
username = 'pyclass'


def device_connect_pm(ip_addr, username):
    '''
    Uses Paramiko to connect to a device given an IP address and a username.
    Asks for the password, opens a connection, invokes the shell and returns
    the handle to the connection
    '''

    port = 22
    password = getpass()
    print "Connecting to: ", ip_addr, "\n"
    remote_conn_pre = paramiko.SSHClient()      # Create ssh client object
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # Accept unknown host keys
    remote_conn_pre.connect(ip_addr, username=username, password=password, 
                            look_for_keys=False, allow_agent=False, port=port)
    remote_conn = remote_conn_pre.invoke_shell()
    return (remote_conn, remote_conn_pre)

def send_command_pm(remote_conn, cmd):
    '''
    Uses Paramkiko to send a command down a previously established SSH channel
    and returns the output
    '''

    print "Sending command: ", cmd, "\n"
    bytesout = remote_conn.send(cmd)
    sleep(1)
    if bytesout:
        return remote_conn.recv(5000)
    else:
        print ("No Data Returned\n")
        return "0"

def config_mode_pm(remote_conn):
    '''
    Uses Paramkiko to enter config mode.
    '''

    print "entering Config Mode...\n"
    out = send_command_pm(remote_conn, "conf t\n")
    if out.endswith("(config)#"):
        print "Config Mode successful. Please be careful\n"
        return 1
    else:
        print "Unable to enter config mode. I'm sorry.\n"
        return 0


def main():
    connection = device_connect_pm(ip_addr, username)
    remote_conn = connection[0]
    if config_mode_pm(remote_conn):
        print "Changing logging buffer...\n"
        output = send_command_pm(remote_conn, "logging buffered 8192\n")
        if output.find("Invalid input") <> -1:
            print "Failed to change logging\n"
        else: print "Logging buffer changed successfully"
    print "End of script.\n"

if __name__ == '__main__':
    main()
