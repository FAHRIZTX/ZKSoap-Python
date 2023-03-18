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


class Fingerprint(object):
    """docstring for Fingerprint"""
    payload = {
        'GetAttLog': '<GetAttLog><ArgComKey xsi:type=\"xsd:integer\">#COMKEY</ArgComKey>#PIN</GetAttLog>',  # noqa: E501
        'GetUserInfo': '<GetUserInfo><ArgComKey xsi:type=\"xsd:integer\">#COMKEY</ArgComKey>#PIN</GetUserInfo>',  # noqa: E501
    }

    def __init__(self, ip: str, port: int = 80, comkey: str = '') -> None:
        super(Fingerprint, self).__init__()
        self.__ip = ip
        self.__port = port
        self.__comkey = comkey
        self.__conn = None
        self.connect()

    def connect(self) -> None:
        try:
            self.__conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__conn.connect((self.__ip, self.__port))
        except Exception as e:
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
        if not data:
            return None

        return self.__parseUserInfoData(data)

    def __parseUserInfoData(self, data) -> List[UserInfo]:
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

    def __send(self, payload: bytes) -> Optional[str]:
        self.__conn.sendall(payload)  # type: ignore
        data = ''
        while True:
            part = self.__conn.recv(1024).decode()  # type: ignore
            if not part:
                break
            data += part
        self.__conn.close()  # type: ignore
        if "<GetUserInfoResponse>" not in data:
            return None

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


a = Fingerprint('103.77.206.42', 80, '987654')
print(a.getStatus())
print(a.getUserInfo('2'))
