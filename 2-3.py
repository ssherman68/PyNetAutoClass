#!\usr\env\python

'''
Python & Network Engineering class week 2 exercise 3:
Convert the code that I wrote here to a class-based solution 
(i.e. convert over from functions to a class with methods).
 -Stacy Sherman 8/11/16
 '''

import telnetlib
import time
import socket
import sys
import getpass

TELNET_PORT = 23
TELNET_TIMEOUT = 5


class DeviceConn(object):
    '''
    Represents a connection to a network device
    
    '''

    def __init__(self, ip, username, password):
        self.ip = ip                     # Management IP address of device
        self.username = username        # Login username
        self.password = password        # Login password
    
    # def telnet_connect(self):
        '''
        Establish telnet connection
        '''
        try:
            self.conn_handle = telnetlib.Telnet(self.ip, TELNET_PORT, TELNET_TIMEOUT)
        except socket.timeout:
            sys.exit("Connection timed-out")

    def login(self):
        '''
        Login to network device
        '''
        output = self.conn_handle.read_until("sername:", TELNET_TIMEOUT)
        self.conn_handle.write(self.username + '\n')
        output += self.conn_handle.read_until("ssword:", TELNET_TIMEOUT)
        self.conn_handle.write(self.password + '\n')
        time.sleep(1)
        return output

    def send_command(self, cmd):
        '''
        Send a command via the telnet connection connect_handle & return
        the output
        '''
        cmd = cmd.rstrip()
        self.conn_handle.write(cmd + '\n')
        time.sleep(1)
        return self.conn_handle.read_very_eager()

    def disable_more(self):
        '''
        Send the "Terminal Length 0" command to disable the more prompt in
        order to read the entire output
        '''
        return self.conn_handle.send_command('terminal length 0')

    def close_conn(self):
        '''
        Closes the telnet connection
        '''
        return self.conn_handle.close()

def main():
    '''
    Write a script that connects to the lab pynet-rtr1, logins, and executes the
    'show ip int brief' command.
    '''
    ip_addr = raw_input("IP address: ")
    ip_addr = ip_addr.strip()
    username = 'pyclass'
    password = getpass.getpass()
    
    my_conn = DeviceConn.telnet_connect(ip_addr, username, password)
    my_conn.login()
    
    time.sleep(1)
    my_conn.read_very_eager()
    my_conn.disable_more()
    
    output = my_conn.send_command('show ip int brief')
    
    print "\n\n"
    print output
    print "\n\n"
    my_conn.close_conn()

if __name__ == "__main__":
    main()
