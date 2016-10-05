#! /usr/bin/env python

import paramiko
from getpass import getpass
from time import sleep

ip_addr = '184.105.247.71'
username = 'pyclass'
port = 22
password = getpass()


def main():
    print "Connecting to: ", ip_addr, "\n"
    remote_conn_pre = paramiko.SSHClient()      # Create ssh client object
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # Accept unknown host keys
    remote_conn_pre.connect(ip_addr, username=username, password=password, 
                            look_for_keys=False, allow_agent=False, port=port)
    remote_conn = remote_conn_pre.invoke_shell()
    cmd = "show version\n"
    print "Sending command: ", cmd, "\n"
    bytesout = remote_conn.send(cmd)
    sleep(1)
    if bytesout:
        shver = remote_conn.recv(5000)
    else:
        print ("No Data Returned\n")
        shver = "0"
    print "Here is the output:\n\n"
    print shver


if __name__ == '__main__':
    main()
