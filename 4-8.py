#! /usr/bin/env python

'''
Python for Network Engineers week 4 exercise 8:

Use Netmiko to change the logging buffer size (logging buffered <size>) and to 
disable console logging (no logging console) from a file on both pynet-rtr1 and 
pynet-rtr2.

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

rtr_list = [pynet1, pynet2]

def main():
    for device in rtr_list:
        rtr_conn = ConnectHandler(**device)
        prompt = rtr_conn.find_prompt()
        rtr_conn.config_mode()
        output = rtr_conn.send_config_from_file(config_file='4_8_cfg.txt')
        print output
    

if __name__ == '__main__':
    main()
