#!/usr/bin/env python

import base64
import requests
import json
import argparse
import getpass
import sys
import re
from collections import Counter
from datetime import datetime

# In a devtest environment, self-signed certs are regularly used.
# Let's disable the warning when over-riding.
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Ask the User for his/her ESM user password
def get_ESM_password(esm_user):
    esm_password = getpass.getpass('Enter password for your ESM username %s: ' % esm_user)
    return esm_password

# Builds the ESM API URL used in all API Call Functions
def build_url(esm):
    url_base = 'https://' + esm + '/rs/esm/'
    return url_base

# ESM Login
def login(url_base, user, password):
    try:
        user = base64.b64encode(user)
        password = base64.b64encode(password)
        params = {"username": user, "password": password, "locale": "en_US", "os" : "Win32"}
        params_json = json.dumps(params)
        login_headers = {'Content-Type': 'application/json'}
        login_response = requests.post(url_base + 'login', params_json, headers=login_headers, verify=False)
        Cookie = login_response.headers.get('Set-Cookie')
        JWTToken = re.search('(^[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*)', Cookie).group(1)
        Xsrf_Token = login_response.headers.get('Xsrf-Token')
        cookie_header = { 'Cookie' : JWTToken }
        #session_header = {'X-Xsrf-Token' : Xsrf_Token, 'Content-Type': 'application/json'}
        session_header = {'Cookie' : JWTToken, 'X-Xsrf-Token' : Xsrf_Token, 'Content-Type': 'application/json'}
    except KeyError:
        print 'Invalid credentials'
        sys.exit(1)
    #return cookie_header, session_header
    return session_header

# ESM Logout
def logout(url_base, session_header):
    requests.delete(url_base + 'logout', headers=session_header, verify=False)

# Writes a list of all Alarms for a built-in Triggered Time Range to CSV
def getAlarms(url_base, session_header, time_range):

    response = requests.post(
        url_base + 'alarmGetTriggeredAlarms?triggeredTimeRange=' + time_range,
        headers=session_header, verify=False)

    data =  response.json()
    alarms = data.get('return')
    counter = dict(Counter(alarm.get('alarmName') for alarm in alarms))
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date =  datetime.now().strftime('%d%b%Y')
    with open('alarm_report_%s.csv' % date, 'w') as f:
        f.write('# Report Generated on %s for the Time Range: %s\n' % (
            current_time, time_range))
        f.write('Alarm Name, Count\n')
        for k, v in counter.items():
            f.write(str(k) + ',' + str(v) + '\n')
        f.close()


# Writes a list of all Alarms for a custom Triggered Time Range to CSV
def getAlarms_custom(url_base, session_header, custom_start, custom_end):

    response = requests.post(
        url_base + 'alarmGetTriggeredAlarms?triggeredTimeRange=CUSTOM&'
                   'customStart=' + custom_start +
                   '&customEnd=' + custom_end,
        headers=session_header, verify=False)

    data =  response.json()
    alarms = data.get('return')
    counter = dict(Counter(alarm.get('alarmName') for alarm in alarms))
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('alarm_report.csv', 'w') as f:
        f.write('# Report Generated on %s for the Time Range: %s to %s\n' % (
        current_time, custom_start, custom_end))
        f.write('Alarm Name, Count\n')
        for k, v in counter.items():
            f.write(str(k) + ',' + str(v) + '\n')
        f.close()

def main():

    # Build Argument List
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description='This is a tool to list  McAfee ESM Triggered Alarms in a CSV Report.')

    #  ESM Parameters
    esm_group = parser.add_argument_group("ESM Options")
    esm_group.add_argument("-e", "--esm", type=str, metavar='ESM HOSTNAME', help="ESM Hostname/ip", required=True)
    esm_group.add_argument("-u", "--esm_user", type=str, metavar='ESM User', help='ESM Username for authentication',
                           required=True)
    esm_group.add_argument("-p", '--esm_password', type=str, metavar='ESM Password', help='ESM User Password')

    # Time Parameters
    time_group = parser.add_mutually_exclusive_group()
    time_group.add_argument("-s", "--standard_timerange", type=str,
                            metavar="Standard Time Range",
                            help="LAST_MINUTE\nLAST_10_MINUTES\n"
                                 "LAST_30_MINUTES\nLAST_HOUR,\nCURRENT_DAY"
                                 "\nPREVIOUS_DAY\nLAST_24_HOURS\nLAST_2_DAYS"
                                 "\nLAST_3_DAYS\nCURRENT_WEEK\nPREVIOUS_WEEK"
                                 "\nCURRENT_MONTH\nPREVIOUS_MONTH"
                                 "\nCURRENT_QUARTER\nPREVIOUS_QUARTER"
                                 "\nCURRENT_YEAR\nPREVIOUS_YEAR")
    time_group.add_argument("-c", "--custom_timerange", type=str,
                            metavar="Custom Time Range",
                            help="Make sure to include both start and end times "
                                 "in the following format (remember the space "
                                 "between each time and enclose within "
                                 "double quotes):\n "
                                 "2019-01-01T00:00:00Z 2019-01-01T23:59:59Z")


    args = parser.parse_args()

    # Prompt for password, if not set
    if args.esm_password is None:
        args.esm_password = get_ESM_password(args.esm_user)

    # Build Session URL
    url = build_url(args.esm)

    # Login and Create ESM Session
    session = login(url, args.esm_user, args.esm_password)

    # Get Alarms using Standard Time Range
    if args.standard_timerange:
        getAlarms(url, session, args.standard_timerange)
        logout(url, session)

    # Get Alarms using Custom Time Range
    if args.custom_timerange:
        if not "T" in args.custom_timerange:
            print "Custom Time Range Must include a T in the Custom Time Range" \
                  "The expected format for each time is 2019-01-01T00:00:00Z"
            sys.exit(1)
        if not "Z" in args.custom_timerange:
            print "Custom Time Range Must include a Z in the Custom Time Range" \
                  "The expected format for each time is 2019-01-01T00:00:00Z"
            sys.exit(1)

        # Split Custom Time Range into Start and End Times
        custom_time = args.custom_timerange.split()
        custom_start = custom_time[0]
        custom_end = custom_time[1]

        getAlarms_custom(url, session, custom_start, custom_end)
        logout(url, session)


if __name__ == '__main__':
    main()