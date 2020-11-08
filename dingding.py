import time
import hmac
import hashlib
import base64
import urllib.parse
import os
import requests


class DingDing:
    def __init__(self, url, secret, prefix=""):
        self.secret = secret
        self.url = url
        self.prefix=prefix

    def send(self, mes, at=None):
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

        res = requests.post(self.url + "&timestamp={}&sign={}".format(timestamp, sign), json={
            "msgtype": "text",
            "text": {
                "content": self.prefix + mes
            },
            "at": {
                "atMobiles": at if at is not None else [],
            }
        })

        print(res.content)


if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv(), override=True)

    ding = DingDing(os.getenv("dingding_url"), os.getenv("dingding_secret"))
    ding.send("测试", at=[os.getenv("phone_number")])
