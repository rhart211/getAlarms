# getAlarms

## Introduction
The main purpose of this tool is to list and count the number of times each configured alarm has been triggered in McAfee ESM.

## Dependencies
Requires [requests](https://github.com/requests/requests)

## Usage
To use this tool:
  run `python getAlarms.py`

You can also get to help by using -h switch:
```
usage: getAlarms.py [-h] -e ESM HOSTNAME -u ESM User [-p ESM Password]
                    [-s Standard Time Range | -c Custom Time Range]

This is a tool to list  McAfee ESM Triggered Alarms in a CSV Report.

optional arguments:
  -h, --help            show this help message and exit
  -s Standard Time Range, --standard_timerange Standard Time Range
                        LAST_MINUTE
                        LAST_10_MINUTES
                        LAST_30_MINUTES
                        LAST_HOUR,
                        CURRENT_DAY
                        PREVIOUS_DAY
                        LAST_24_HOURS
                        LAST_2_DAYS
                        LAST_3_DAYS
                        CURRENT_WEEK
                        PREVIOUS_WEEK
                        CURRENT_MONTH
                        PREVIOUS_MONTH
                        CURRENT_QUARTER
                        PREVIOUS_QUARTER
                        CURRENT_YEAR
                        PREVIOUS_YEAR
  -c Custom Time Range, --custom_timerange Custom Time Range
                        Make sure to include both start and end times in the following format (remember the space between each time and                         enclose within double quotes): 2019-01-01T00:00:00Z 2019-01-01T23:59:59Z

ESM Options:
  -e ESM HOSTNAME, --esm ESM HOSTNAME
                        ESM Hostname/ip
  -u ESM User, --esm_user ESM User
                        ESM Username for authentication
  -p ESM Password, --esm_password ESM Password
                        ESM User Password
```
