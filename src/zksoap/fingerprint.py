import datetime
import socket
from typing import Union, Optional, List
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

class Fingerprint(object):

    payload = {
        'GetAttLog': '<GetAttLog><ArgComKey xsi:type=\"xsd:integer\">#COMKEY</ArgComKey>#PIN</GetAttLog>',  # noqa: E501
        'GetUserInfo': '<GetUserInfo><ArgComKey xsi:type=\"xsd:integer\">#COMKEY</ArgComKey>#PIN</GetUserInfo>',  # noqa: E501
    }

    def __init__(self, ip: str, port: int = 80, comkey: str = '') -> None:
        super(Fingerprint, self).__init__()
        self.__ip = ip
        self.__port = port if isinstance(port, int) else int(port)
        self.__comkey = comkey
        self.__conn = None
        self.connect()

    def connect(self) -> None:
        try:
            self.__conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__conn.connect((self.__ip, self.__port))
        except Exception:
            raise Exception("Can't Connect")

    def getStatus(self) -> str:
        return 'connected' if self.__conn else 'disconnected'

    def getUserInfo(self, pin: Union[str, list] = "all") -> Optional[list]:
        self.connect()
        if isinstance(pin, list):
            listpin = ""
            for pinid in pin:
                listpin += "<Arg><PIN>"+pinid+"</PIN></Arg>"
            pin = listpin
        else:
            pin = "<Arg><PIN>"+pin+"</PIN></Arg>"
        payload = self.__generatePayload(
            'GetUserInfo',
            {'key': "#PIN", 'value': pin}
        )
        data = self.__send(payload)
        if "<GetUserInfoResponse>" not in data:
            return None

        return self.__parseUserInfoData(data)

    def __parseUserInfoData(self, data: str) -> List[UserInfo]:
        datas = data.split("<Row>")
        datas.pop(0)

        userData = []
        for dataRow in datas:
            fid = self.__getValueFromTag(
                dataRow,
                "<PIN>",
                "</PIN>"
            )
            name = self.__getValueFromTag(
                dataRow,
                "<Name>",
                "</Name>"
            )
            password = self.__getValueFromTag(
                dataRow,
                "<Password>",
                "</Password>"
            )
            group = self.__getValueFromTag(
                dataRow,
                "<Group>",
                "</Group>"
            )
            privilege = self.__getValueFromTag(
                dataRow,
                "<Privilege>",
                "</Privilege>"
            )
            card = self.__getValueFromTag(
                dataRow,
                "<Card>",
                "</Card>"
            )
            pin2 = self.__getValueFromTag(
                dataRow,
                "<PIN2>",
                "</PIN2>"
            )

            user = UserInfo(
                pin=fid,
                name=name,
                password=password,
                group=group,
                privilege=privilege,
                card=card,
                pin2=pin2
            )
            userData.append(user)
        return userData

    def getAttendance(
        self,
        pin: Union[str, list] = "all",
        date_start: Optional[str] = None,
        date_end: Optional[str] = None
    ):
        self.connect()
        if date_start is not None and date_end is None:
            date_end = date_start

        if isinstance(pin, list):
            listpin = ""
            for pinid in pin:
                listpin += "<Arg><PIN>"+pinid+"</PIN></Arg>"
            pin = listpin
        else:
            pin = "<Arg><PIN>"+pin+"</PIN></Arg>"

        payload = self.__generatePayload(
            'GetAttLog',
            {'key': "#PIN", 'value': pin}
        )
        data = self.__send(payload)

        if "<GetAttLogResponse>" not in data:
            return None
        return self.__parseAttendanceData(data, date_start, date_end)

    def __parseAttendanceData(
        self,
        data: str,
        date_start: Optional[str] = None,
        date_end: Optional[str] = None
    ) -> List[UserAttendance]:
        datas = data.split("<Row>")
        datas.pop(0)

        userData = []
        for dataRow in datas:
            fid = self.__getValueFromTag(
                dataRow,
                "<PIN>",
                "</PIN>"
            )
            dt = self.__getValueFromTag(
                dataRow,
                "<DateTime>",
                "</DateTime>"
            )
            verified = self.__getValueFromTag(
                dataRow,
                "<Verified>",
                "</Verified>"
            )
            status = self.__getValueFromTag(
                dataRow,
                "<Status>",
                "</Status>"
            )
            workcode = self.__getValueFromTag(
                dataRow,
                "<WorkCode>",
                "</WorkCode>"
            )

            if date_start is not None and date_end is not None:
                DR = self.__dateRange(date_start, date_end)

                dateCheck = dt.split(" ")[0];

                if dateCheck in DR:
                    user = UserAttendance(
                        pin=fid,
                        datetime=dt,
                        verified=verified,
                        status=status,
                        workcode=workcode,
                    )
                    userData.append(user)
            else:
                user = UserAttendance(
                    pin=fid,
                    datetime=dt,
                    verified=verified,
                    status=status,
                    workcode=workcode,
                )
                userData.append(user)
        return userData 

    def __send(self, payload: bytes) -> Optional[str]:
        self.__conn.sendall(payload)  # type: ignore
        data = ''
        while True:
            part = self.__conn.recv(1024).decode()  # type: ignore
            if not part:
                break
            data += part
        self.__conn.close()  # type: ignore
        return data

    def __generatePayload(self, payload_name: str, data: dict) -> bytes:
        payload = self.payload[payload_name]
        payload = payload.replace("#COMKEY", self.__comkey)
        payload = payload.replace(data['key'], data['value'])

        payload = f"POST /iWsService HTTP/1.0\r\nContent-Type: text/xml\r\nContent-Length: {len(payload)}\r\n\r\n{payload}\r\n"  # noqa: E501
        return bytes(payload, 'utf-8')

    def __getValueFromTag(self, data, start, end):
        res = data.split(start)[1].split(end)[0]
        return res

    def __dateRange(self, startDate: str, endDate: str) -> List[str]:
        start = datetime.datetime.strptime(startDate, "%Y-%m-%d")
        end = datetime.datetime.strptime(endDate, "%Y-%m-%d")
        date_generated = [
            (start + datetime.timedelta(days=x)).strftime("%Y-%m-%d")
            for x in range(0, (end-start).days+1)
        ]
        return date_generated
