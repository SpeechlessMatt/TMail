import json
import re
import requests
from loguru import logger

class TMail:
    HEADERS = {
        "Referer": "http://24mail.chacuo.net/",
        "Host": "24mail.chacuo.net",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    }

    def __init__(self) -> None:
        self._url = "http://24mail.chacuo.net/"
        self.session = requests.session()
        self.account = None

    def __del__(self) -> None:
        self.session.close()

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, _url):
        logger.trace(f"将url源头更改为{_url}")
        self._url = _url

    def get_account(self) -> str|None:
        """获取临时邮箱名称，返回邮箱名称，也可以用 Tmail.account 访问该属性"""
        resp = self.session.get(self.url, headers=self.HEADERS, timeout=5)
        obj = re.compile(r'<input.*?name="converts".*?value="(.*?)"', re.S)
        origin_data = obj.findall(resp.text)[0]
        # 客户端返回json数据中：{...,data:[邮箱]}
        self.account = origin_data

        if self.account == "False":
            self.account = None
            return None

        return self.account + "@chacuo.net"

    def get_email_list(self, details=False) -> list|dict:
        """
        刷新收件箱,返回收件箱
        Args:
            details: 为True则返回邮件列表，为False则返回字典

        """
        params = {
            "data": self.account,
            "type": "refresh",
            "arg": ""
        }
        resp = self.session.post(self.url, params=params, headers=self.HEADERS)
        # json 加载
        data = json.loads(resp.text)
        logger.debug(data)
        status = data["status"]
        # 接口处使用列表形式处理
        child_data = data["data"][0]
        email_list = child_data["list"]
        num = child_data["user"]["NUM"]
        if details:
            return {"status": status, "email_list": email_list, "num": num}
        else:
            # 'list': [{'UID': , 'TO': '', 'PATCH': , 'ISREAD': , 'SENDTIME': '', 'FROM': ', 'SUBJECT': '', 'MID': , 'SIZE': 2410}]
            return email_list

    def read_mail(self, MID: str) -> tuple:
        """
        读取邮件信息
        :param MID: 邮件ID -可以通过get_email_list()方法拿到
        :return: (status: 状态码, email_info: 邮件信息, email_detail: 邮件正文）
        """
        params = {
            "data": self.account,
            "type": "mailinfo",
            "arg": f"f={MID}"
        }
        resp = self.session.post(self.url, params=params, headers=self.HEADERS)
        logger.debug(resp.text)
        # json 加载
        origin_datas = json.loads(resp.text)
        status = origin_datas["status"]
        email_data = origin_datas["data"][0]
        # 邮件简介
        email_info = email_data[0]
        # 邮件正文，包含富文本和普通文本
        email_detail = email_data[1]
        return status, email_info, email_detail


    def delete_mail(self, MID: str) -> bool:
        """
        事实上不需要手动删除邮件，暂时不需要维护这个函数
        :param MID: 邮件ID
        :return: True/False
        """
        try:
            params = {
                "data": self.account,
                "type": "delmail",
                "arg": f"f={MID}"
            }
            resp = self.session.post(self.url, params=params)
            logger.debug(resp.text)
            return True
        except Exception as e:
            logger.warning(e)
            return False

    def close(self):
        self.__del__()