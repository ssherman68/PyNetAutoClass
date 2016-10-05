#! /usr/bin/env python

'''
Using SNMPv3 create a script that detects router configuration changes.

If the running configuration has changed, then send an email notification to
yourself identifying the router that changed and the time that it changed.
'''


import time
import datetime
from snmp_helper import snmp_get_oid_v3, snmp_extract

AUTH_KEY = 'galileo1'
ENCRYPT_KEY = 'galileo1'
SNMP_USERNAME = 'pysnmp'
SNMP_PORT = 161
IP = '184.105.247.71'
OID_RUNNINGLASTCHANGED = '1.3.6.1.4.1.9.9.43.1.1.1.0'
OID_SYSUPTIME = '1.3.6.1.2.1.1.3.0'
MONITOR_CANCEL = 8640000                  # Set monitor time to 24 hours
E_ADDR = 'ssherman68@gmail.com'


def get_last_change():
    user = (SNMP_USERNAME, AUTH_KEY, ENCRYPT_KEY)
    rtr2 = (IP, SNMP_PORT)
    print "Getting last change...\n\n"
    return int(snmp_extract(snmp_get_oid_v3(rtr2, user, OID_RUNNINGLASTCHANGED)))


def conv_tticks(timestamp):
    '''
    Converts a (Cisco) timestamp in 100ths of a second into a time delta with
    days, hours, minutes and seconds. Returns the timedelta.
    Note: assumes a max 32 bit value where the max value would be 4,294,967,296
    100ths of a second or 1 year, 132 days, 2 hours, 27 minutes & 52 seconds
    '''

    print "Converting Timestamp...\n\n"
    if timestamp > 4294967296:
        print "Error: Timestamp out of range"
        null_timestamp = datetime.timedelta()
        return null_timestamp
    else:
        ttsecs = timestamp/100                                  # Convert to seconds
        days, secs2 = divmod(ttsecs, 86400)                  # Convert to days & remainder
        hours, secs3 = divmod(secs2, 3600)                  # Convert to hours & remainder
        mins, secs = divmod(secs3, 60)                        # Convert to minutes & seconds
        timestamp_td = datetime.timedelta(days=days, seconds=secs, hours=hours, minutes=mins)
        return timestamp_td

def calc_time(timestamp):
    '''
    Takes a Cisco uptime stamp in 1/100ths of a second and converts it to a date
    and time. Assumes the given timestamp is less than a minute old.

    timestamp = uptime of last config change
    current_uptime = timenow
    how_long = current_uptime - time_of_change
    *Convert how_long to time delta
    *Change conversion to days & return time delta, not tuple. Drop the years
    when_change = time_now_td - how_long_ago_td
    '''
    print "Calculating Time...\n\n"
    user = (SNMP_USERNAME, AUTH_KEY, ENCRYPT_KEY)
    rtr2 = (IP, SNMP_PORT)
    current_uptime = int(snmp_extract(snmp_get_oid_v3(rtr2, user, OID_SYSUPTIME)))
    how_long_ago = (current_uptime - timestamp)
    t = datetime.datetime.now()
    how_long_ago_td = conv_tticks(how_long_ago)
    time_now_td = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second)
    print "Time Now Delta: ", time_now_td, "\n"
    print "How Long Ago Delta: ", how_long_ago_td, "\n"
    time_of_change = time_now_td - how_long_ago_td
    return time_of_change


def send_email(change_time):
    '''
    Uses snmplib and the Kirk Byers email_helper library to send an email. Requires an SMTP server.
    '''
    import email_helper

    recipient = E_ADDR
    subject = "Config has changed"
    message = "The configuration changed today at: %s" % change_time 
    sender = "ssherman@gnf.org"
    email_helper.send_mail(recipient, subject, message, sender)


def main():
                                             # Get last cfg change as a baseline
    last_cfg_change = get_last_change()
    print "Last Config Change time is: ", last_cfg_change
    run_time = 0                        # Set run time of monitor to 0
    while run_time <= MONITOR_CANCEL:
        print "Sleeping..."
        time.sleep(60)                  # Poll every minute
        new_cfg_change = get_last_change()
        print "New Config Change time is: ", new_cfg_change
        delta = new_cfg_change - last_cfg_change
        if delta > 0:
            last_cfg_change = new_cfg_change
            change_time = calc_time(new_cfg_change)
            print "Change Time is: "
            print change_time, "\n"
        #   send_mail(E_ADDR, change_time)

if __name__ == '__main__':
    main()

