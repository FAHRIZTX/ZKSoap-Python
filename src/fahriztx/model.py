from dataclasses import dataclass


@dataclass
class UserInfo:
    pin: str
    name: str
    password: str
    group: str
    privilege: str
    card: str
    pin2: str

@dataclass
class UserAttendance:
    pin: str
    datetime: str
    verified: str
    status: str
    workcode: str
