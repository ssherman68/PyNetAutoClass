#! /usr/bin/env python

'''
Python & Network Automation class week 2 exercise 4.
Create a script that connects to both pynet-rtr1 and pynet-rtr2 and prints out
both the MIB2 SysName and SysDescr

'''
# Import any modules

from snmp_helper import snmp_get_oid,snmp_extract

COMMUNITY_STRING = 'galileo'
SNMP_PORT = 161
ROUTERS = ('184.105.247.70','184.105.247.71')
OIDS = ('1.3.6.1.2.1.1.5.0', '1.3.6.1.2.1.1.1.0')


def print_oid(ip, COMMUNITY_STRING, SNMP_PORT, oid):
    a_device = (ip, COMMUNITY_STRING, SNMP_PORT)
    snmp_data = snmp_get_oid(a_device, oid)
    output = snmp_extract(snmp_data)
    print "\n", output

def main():
    print "\n\n =================OID Output===============\n\n"
    for ip in ROUTERS:
        print "\n Router IP", ip
        print "\n"
        for oid in OIDS:
            print_oid(ip, COMMUNITY_STRING, SNMP_PORT, oid)
    print "\n\n =======================================\n\n"



if __name__ == '__main__':
    main()
