#! /usr/bin/env python

'''
Using Arista's pyeapi, create a script that allows you to add a VLAN (both the VLAN ID and the VLAN name).

Your script should first check that the VLAN ID is available and only add the VLAN if it doesn't already exist.
use VLAN IDs between 100 and 999.  You should be able to call the script from the command line as follows:

   python eapi_vlan.py --name blue 100     # add VLAN100, name blue

If you call the script with the --remove option, the VLAN will be removed.

   python eapi_vlan.py --remove 100          # remove VLAN100

Once again only remove the VLAN if it exists on the switch.  You will probably want to use Python's
 argparse to accomplish the argument processing.
'''

# Import any modules

import pyeapi
import argparse

def vlan_exist(myswitch, vid):
    # Given the VLAN ID (vid), check to see if the vlan already exists.
    # return 1 if it already exists, return 0 if it does not exist.

    vid = str(vid)
    try:
        cmd_result = myswitch.enable('show vlan')
        cmd_result = cmd_result[0]
        vlans = cmd_result['result']['vlans']
        if vid in vlans:
            return 1
    except (pyeapi.eapilib.CommandError, KeyError):
        pass
    return 0


def vlan_remove(myswitch, vid):
    '''
    Remove the VLAN given in vid from the switch.
    '''
    if vlan_exist(myswitch, vid):
        cmd_str = "no vlan " + str(vid)
        print "Removing VLAN {0}... ".format(vid)
        cmd_result = myswitch.config(['configure terminal', cmd_str])
        return 0
    else:
        return 1


def vlan_add(myswitch, vid, name):
    '''
    Remove the VLAN given in vid from the switch.
    '''
    if not vlan_exist(myswitch, vid):
        cmd_str = "vlan " + str(vid)
        cmd_str2 = "name " + name
        print "Adding VLAN {0} with name {1}... ".format(vid, name)
        cmd_result = myswitch.config(['configure terminal', cmd_str, cmd_str2])
        return 0
    else:
        print "VLAN {0} already exists. Leaving the configuration as-is".format(vid)
        return 1


def main():
    parser = argparse.ArgumentParser(description='Add or Remove VLANs')
    parser.add_argument('--name', help="Specify '--name' to add a VLAN. Optionally enter the name after '--name' ",
                        action='store', dest='name')
    parser.add_argument('--remove', help="Specify '--remove' to remove the VLAN. Enter the VLAN ID after '--remove'",
                        action='store_true')
    parser.add_argument("vid", help="Numerical VLAN ID of the VLAN you want to add or remove", type=int)
    args = parser.parse_args()
    print "\nargs = {}\n".format(args)
    name = args.name
    vid = args.vid
    remove=args.remove
    myswitch = pyeapi.connect_to("pynet-sw1")
    if name:
        va_fail = vlan_add(myswitch, vid, name)
    elif remove:
        vr_fail = vlan_remove(myswitch, vid)
    else:
        print "\nI'm not sure what you want me to do"
        return 0




if __name__ == '__main__':
    main()
