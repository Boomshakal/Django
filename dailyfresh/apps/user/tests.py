# Create your tests here.
from typing import Any
import base64
import hashlib
import hmac
import struct
import time

import pyotp
from qrcode import QRCode
from qrcode import constants


# 利用参数secretKey,计算Google Authenticator 6位动态码。
def getMFACode(Secret):
    print('MFA密钥:{}'.format(Secret))
    K = base64.b32decode(Secret, True)
    C = struct.pack(">Q", int(time.time()) // 30)
    H = hmac.new(K, C, hashlib.sha1).digest()
    O = H[19] & 15  # bin(15)=00001111=0b1111
    DynamicPasswd = str((struct.unpack(">I", H[O:O + 4])[0] & 0x7fffffff) % 1000000)
    TOTP = str(0) + str(DynamicPasswd) if len(DynamicPasswd) < 6 else DynamicPasswd
    print('动态MFA:{}'.format(TOTP))
    return TOTP


def getMFAImg(name, Secret):
    # otpauth://totp/  固定格式
    # name：标识符信息，issuer：发行信息
    url = "otpauth://totp/" + name + "?secret=%s" % Secret + "&issuer=Anchnet"
    qr = QRCode(version=1, error_correction=constants.ERROR_CORRECT_L, box_size=6, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    img.show()


def checkCode(str):
    code = input('输入验证码:')
    t = pyotp.TOTP(str)
    result = t.verify(code)
    msg = result if result is True else False
    print('验证码验证{}'.format(msg))
    return msg


if __name__ == '__main__':
    name = 'user01' + ':SmartMS'
    # Secret = pyotp.random_base32()
    secret = 'UFB6R5QKLPV7FGIU'
    getMFACode(secret)
    getMFAImg(name, secret)
    checkCode(secret)


