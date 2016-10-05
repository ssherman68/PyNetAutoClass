#! /usr/bin/env python

'''
6. Use threads and Netmiko to execute 'show version' on each device in the 
database. Calculate the amount of time required to do this. What is the 
difference in time between executing 'show version' sequentially versus using 
threads?

'''
# Import modules

from netmiko import ConnectHandler
from net_system.models import NetworkDevice, Credentials
from datetime import datetime
import django
import threading

def show_ver(dev, final_output):
    device_type = dev.device_type
    port = dev.port
    secret = ''
    ip = dev.ip_address
    creds = dev.credentials
    username = creds.username
    password = creds.password
    remote_conn = ConnectHandler(device_type=device_type, ip=ip, username=username, password=password, port=port)
    final_output += "#" * 80
    final_output += "\n{}\n\n".format(dev.device_name)
    final_output += remote_conn.send_command_expect("show version")
    print final_output

def main():
    django.setup()
    devices = NetworkDevice.objects.all()   # get all the devices
    starttime = datetime.now()
    final_output = ''
    for dev in devices:
        sh_ver_thread = threading.Thread(target=show_ver, args=(dev, final_output,))
        sh_ver_thread.start()
    main_thread = threading.currentThread()
    for t in threading.enumerate():
        if t != main_thread:
            t.join()
    print final_output
    endtime = datetime.now()
    totaltime = endtime - starttime
    print "\n Total time: {} seconds\n".format(totaltime.seconds)


if __name__ == '__main__':
    main()
