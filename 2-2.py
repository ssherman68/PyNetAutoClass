#! /usr/bin/env python

'''
Python & Network Automation class week 2 exercise 2
-Stacy Sherman 8/8/16

Write a script that connects using telnet to the pynet-rtr1 router. 
Execute the 'show ip int brief' command on the router and return the 
output.

'''

import telnetlib
import time

def telnet_connect(ip_addr, username, password, TELNET_PORT, TELNET_TIMEOUT):
    print "Connecting to {0} on port {1}...".format (ip_addr, TELNET_PORT)
    conn_handle = telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)   
    conn_handle.read_until('rname: ', TELNET_TIMEOUT)
    print "Sending username..."
    conn_handle.write(username + '\n')
    conn_handle.read_until('ssword: ', TELNET_TIMEOUT)
    print "Sending password..."
    conn_handle.write(password + '\n')
    print "Setting terminal lenth to 0..."
    conn_handle.write ("terminal length 0" + '\n')   # Get rid of "More" prompt
    time.sleep(1)                                   # Wait for one second
    output = conn_handle.read_very_eager()          # Read all output
    print output
    return conn_handle


def telnet_send_cmd(conn_handle, cmd):
    cmd = cmd.rstrip()
    print "Sending command: {0}...\n ".format (cmd)
    conn_handle.write(cmd + '\n')
    time.sleep(1)
    output = conn_handle.read_very_eager()
    return output


def main():
    ip_addr = '184.105.247.70'
    username = 'pyclass'
    password = '88newclass'
    TELNET_PORT = 23
    TELNET_TIMEOUT = 5
    cmd = 'show ip interface brief'

    conn_handle = telnet_connect(ip_addr, username, password, TELNET_PORT, TELNET_TIMEOUT)
    output = telnet_send_cmd(conn_handle, cmd)
    print output
    conn_handle.close()

if __name__ == '__main__':
    main()
