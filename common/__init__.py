# - coding: utf-8  -
from yubico.yubico import Yubico
from yubico.yubico_exceptions import YubicoError

yubico = Yubico('10516', 'B0IpBq0fiNLHeEwbGMhVZuxofLg=')

def verify_yubikey(otp):
    try:
        return yubico.verify(otp)
    except YubicoError:
        return  False
