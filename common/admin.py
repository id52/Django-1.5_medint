# - coding: utf-8  -
from django.conf import settings
from common.models import YubiKey, StaffRole, MedintUser  #, Document
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class YudiKeyAdmin (admin.ModelAdmin):
    fields = ('role', 'user', 'uid')


class DocumentAdmin(admin.ModelAdmin):
    change_form_template = 'admin/common/document_form.html'


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MedintUser


class MedintUserAdmin(UserAdmin):
    list_display = ('username',)
    fieldsets = (
        (None, {'fields': ('password',)}),
        # ('Personal info', {'fields': ('date_of_birth',)}),
        # ('Permissions', {'fields': ('is_admin',)}),
        # ('Important dates', {'fields': ('last_login',)}),
    )

admin.site.register(YubiKey)
admin.site.register(StaffRole)
admin.site.register(MedintUser, MedintUserAdmin)
# admin.site.register(Document, DocumentAdmin)
