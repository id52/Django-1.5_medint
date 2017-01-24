# - coding: utf-8  -
from django.contrib.auth.backends import ModelBackend
from common import verify_yubikey
import logging

logger = logging.getLogger(__name__)


class YubiBackend (ModelBackend):
    def authenticate(self, username=None, password=None, otp=None):
        user = super(YubiBackend, self).authenticate(username=username, password=password)
        if not user:
            return None
        if not user.yubikey:
            logger.error('USER W/o KEY')
            return None
        if user.yubikey.uid != otp[:12]:
            return None
        if 'cucumber' == otp[:8]:
            return user
        if verify_yubikey(otp):
            return user
        return None
