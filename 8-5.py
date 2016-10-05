#! /usr/bin/env python

'''
5. Use Netmiko to connect to each of the devices in the database. 
Execute 'show version' on each device. Calculate the amount of time required 
to do this. Note, your results will be more reliable if you use Netmiko's 
send_command_expect() method. There is an issue with the Arista vEOS switches 
and Netmiko's send_command() method.

'''
# Import modules

from netmiko import ConnectHandler
from net_system.models import NetworkDevice, Credentials
from datetime import datetime
import django


def main():
    django.setup()
    
    devices = NetworkDevice.objects.all()   # get all the devices
    starttime = datetime.now()
    for dev in devices:
        device_type = dev.device_type
        port = dev.port
        secret = ''
        ip = dev.ip_address
        creds = dev.credentials
        username = creds.username
        password = creds.password
        remote_conn = ConnectHandler(device_type=device_type, ip=ip, username=username, password=password, port=port)
        print remote_conn.send_command_expect("show version")
    endtime = datetime.now()
    totaltime = endtime - starttime
    print "\n Total time: {}".format(totaltime.seconds)


if __name__ == '__main__':
    main()
