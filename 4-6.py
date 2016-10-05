#! /usr/bin/env python

'''
Python for Network Engineers week 4 exercise 6:

Use Netmiko to execute 'show arp' on pynet-rtr1, pynet-rtr2, and juniper-srx.

Stacy Sherman 8/24/16

'''

from netmiko import ConnectHandler

pynet1 = {
    'device_type': 'cisco_ios',
    'ip': '184.105.247.70',
    'username': 'pyclass',
    'password': '88newclass',
}


pynet2 = {
    'device_type': 'cisco_ios',
    'ip': '184.105.247.71',
    'username': 'pyclass',
    'password': '88newclass',
}

pynet3 = {
    'device_type': 'juniper',
    'ip': '184.105.247.76',
    'username': 'pyclass',
    'password': '88newclass',
}

rtr_list = [pynet1, pynet2, pynet3]

def main():
    for device in rtr_list:
        rtr_conn = ConnectHandler(**device)
        output = rtr_conn.send_command("show arp")
        print device['ip'], " ARP Table:\n"
        print "==========================================================="
        print output, "\n"
    

if __name__ == '__main__':
    main()
