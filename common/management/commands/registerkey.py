# - coding: utf-8  -
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from common.models import YubiKey


class Command(BaseCommand):
    def handle(self, *args, **options):

        if len(args) == 0:
            username = raw_input('Enter username: ').strip()
        else:
            username = args[0]

        try:
            user = User.objects.get(username__iexact=username)
        except User.DoesNotExist:
            self.stderr.write('User does not exist\n')
            return
        else:
            r = raw_input('press key on the key : ')
            if YubiKey.objects.all().filter(user=user).exists():
                user.yubikey = YubiKey.objects.create(uid=r[:12], role=user.role)
            else:
                YubiKey.objects.create(user=user, uid=r[:12], role=user.role)
