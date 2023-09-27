ZK Soap Python Library
======

A Python Library For Manage Data From Fingerprint Machine with SOAP Protocol

## Features

 * Get Attendance Log with DateRange
 * Get User Information

## Requirements

 * Python version 3.6 or higher
 * Fingerprint Machine Support ZK Web Service

## Easy Installation

### Install with pip

To install with `pip`, simply require the
latest version of this package.

```bash
python -m pip install zksoap
```

## Quick Start

Just pass your IP, Port and Comkey :

* Get Attendance

```python
# reference the ZK Soap PHP namespace
from zksoap import Fingerprint

# initial
machine = Fingerprint('192.168.1.175', '80', '123456')

# get machine status
print("Machine Status : "+machine.getStatus()) # connected | disconnected

# get all log data
print(machine.getAttendance()) # return List of Attendance Log

# get all log data with date
print(machine.getAttendance('all', '2022-05-01')) # return List of Attendance Log

# get all log data with date range
print(machine.getAttendance('all', '2022-05-01', '2022-05-10')) # return List of Attendance Log

# get specific pin log data
print(machine.getAttendance('1')) # return List of Attendance Log
# OR List
print(machine.getAttendance(['1', '2'])) # return List of Attendance Log

# get exported json format
user_attendance_data = machine.getAttendance()
json_data = json.dumps(user_attendance_data, cls=UserAttendanceEncoder, indent=4)
file_path = 'user_attendance2.json'
with open(file_path, 'w') as file:
    file.write(json_data)

print(f"JSON data for user attendance saved to {file_path}")

```

* Get User Information

```python
# reference the ZK Soap PHP namespace
from zksoap import Fingerprint

# initial
machine = Fingerprint('192.168.1.175', '80', '123456')

# get machine status
print("Machine Status : "+machine.getStatus()) # connected | disconnected

# get all user data
print(machine.getUserInfo()) # return List of User Info Data

# get specific pin user data
print(machine.getUserInfo('1')) # return List of User Info Data
# OR List
print(machine.getUserInfo(['1', '2'])) # return List of User Info Data

# get exported json format
decoded_data = machine.getUserInfo()
data_dict = {"data": decoded_data}
json_data = json.dumps(data_dict, indent=4, cls=UserInfoEncoder)
file_path = 'user_info2.json'
with open(file_path, 'w') as file:
    file.write(json_data)

print(f"JSON data saved to {file_path}")

```

## Changelog

* Uploading to pypi
