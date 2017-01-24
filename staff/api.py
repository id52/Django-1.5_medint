# - coding: utf-8  -
import logging
from django import forms
from common.models import MedintUser, UserInfo, YubiKey, ROLES
from jsonview import JSONView, make_response
from medint.forms import BaseRegisterForm


class RegisterForm(BaseRegisterForm):
    staff_role = forms.CharField(label='')
    password = forms.CharField(label='')
    yubiid = forms.CharField(label='')


class RegisterView(JSONView):

    def __validate_params__(self, username, mail, uid, role):
        if UserInfo.objects.filter(email__iexact=mail).exists():
            return 'This email already exists! Please try again or recover the password for the email address given.'
        if MedintUser.objects.filter(username__iexact=username).exists():
            return 'This username already exists! Please try again or recover the password for the email address given.'
        try:
            yubikey = YubiKey.objects.get(uid=uid, role=role, user=None)
        except YubiKey.DoesNotExist:
            return 'Unknown yubikey'

    def post(self, request):
        f = RegisterForm(request.POST)
        if f.is_valid():
            mail = f.cleaned_data['email'].lower()
            username = f.cleaned_data['username'].lower()
            err = self.__validate_params__(username, mail, f.cleaned_data['yubiid'], ROLES['STAFF']['id'])
            if err:
                return make_response(error=err)

            u = MedintUser.objects.create_staff(
                f.cleaned_data['username'],
                email=mail,
                password=f.cleaned_data['password'],
                first_name=f.cleaned_data['firstname'],
                last_name=f.cleaned_data['lastname'],
                phone=f.cleaned_data['phone'],
                uid=f.cleaned_data['yubiid'],
                staff_role=int(f.cleaned_data['staff_role'])
            )
            return make_response()
        else:
            logging.error(f._errors)
            return make_response(validation=f._errors)


class KeyView(JSONView):
    def get(self, request, parent=None):
        keys = []
        if parent:
            for k in YubiKey.objects.select_related('user', 'user__user_info').filter(creator=request.user).filter(
                    role=ROLES['PATIENT']['id']).filter(parent=parent):
                key = {'uid': k.uid}
                if k.user:
                    u = k.user
                    key['user'] = {'id': u.id, 'username': u.username, 'firstName': u.user_info.first_name,
                                   'lastName': u.user_info.last_name}
                keys.append(key)
        else:
            for k in YubiKey.objects.select_related('user', 'user__user_info').filter(creator=request.user).filter(
                    role=ROLES['DOCTOR']['id']):
                key = {'uid': k.uid}
                if k.user:
                    u = k.user
                    key['user'] = {'id': u.id, 'username': u.username, 'firstName': u.user_info.first_name,
                                   'lastName': u.user_info.last_name}
                keys.append(key)
        return make_response(keys)

    def post(self, request, parent=None):
        uid = request.POST.get('uid')[:12]
        if YubiKey.objects.filter(uid=uid):
            return make_response(error='This key is already registered')

        role = int(request.POST.get('role'))
        if parent:
            parent_user = MedintUser.objects.get(id=parent)
            YubiKey.objects.create(uid=uid, role=role, creator=request.user, parent=parent_user)
        else:
            YubiKey.objects.create(uid=uid, role=role, creator=request.user)
        return make_response()