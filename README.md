# getAlarms

## Introduction
The main purpose of this tool is to list and count the number of times each configured alarm in McAfee ESM has been triggered.

## Dependencies
Requires [requests](https://github.com/requests/requests)

## Usage
To get the usage for this tool:
  run `python getAlarms.py -h`

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
                        Make sure to include both start and end times in the following format 
                        (remember the space between each time and enclose within double quotes): 
                        2019-01-01T00:00:00Z 2019-01-01T23:59:59Z

ESM Options:
  -e ESM HOSTNAME, --esm ESM HOSTNAME
                        ESM Hostname/ip
  -u ESM User, --esm_user ESM User
                        ESM Username for authentication
  -p ESM Password, --esm_password ESM Password
                        ESM User Password
```

## Usage Examples:

### Specifying the User Password
`python getAlarms.py -e ESM IP or FQDN -u my_user -p my_password -s CURRENT_YEAR`

### Without Specifying the User Password
`python getAlarms.py -e ESM IP or FQDN -u my_user -s CURRENT_YEAR`
- If no password is specified in the command line, the tool will prompt you for the specified user's password.

