#! /usr/bin/env python

'''
Python for Network Engineers week 4 exercise 1:

Use Paramiko to retrieve the entire 'show version' output from pynet-rtr2.

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
    print "Bytes received: ",bytesout,"\n"
    if bytesout:
        return remote_conn.recv(5000)
    else:
        print ("No Data Returned\n")
        return "0"


def main():
    connection = device_connect_pm(ip_addr, username)
    remote_conn = connection[0]
    send_command_pm(remote_conn, "term len 0\n")
    cmd = "show version\n"
    shver = send_command_pm(remote_conn, cmd)
    print "Here is the output:\n\n"
    print shver


if __name__ == '__main__':
    main()
