#! /usr/bin/env python

'''
ython for Network Engineers week 4 exercise 4:

Use Netmiko to enter into configuration mode on pynet-rtr2. Also use Netmiko 
to verify your state (i.e. that you are currently in configuration mode).

Stacy Sherman 8/24/16

'''

from netmiko import ConnectHandler
from getpass import getpass

pynet2 = {
    'device_type': 'cisco_ios',
    'ip': '184.105.247.71',
    'username': 'pyclass',
    'password': '88newclass',
}


def main():
    password = getpass
    pynet_rtr2 = ConnectHandler(**pynet2)
    pynet_rtr2.config_mode()
    if pynet_rtr2.check_config_mode(): 
        print "You are in config mode.\n"
    else:  
        print "Config mode failed.\n"



if __name__ == '__main__':
    main()
