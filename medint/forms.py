# - coding: utf-8  -
from django import forms


class DivForm(forms.Form):
    def as_div(self):
#        "Returns this form rendered as HTML <li>s -- excluding the <ul></ul>."
        return self._html_output(
            normal_row=u'<li%(html_class_attr)s>%(errors)s%(label)s %(field)s%(help_text)s</li>',
            error_row=u'<li>%s</li>',
            row_ender='</li>',
            help_text_html=u' <span class="helptext">%s</span>',
            errors_on_separate_row=False)


class BaseRegisterForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput({"placeholder": "Please choose a username"}))
    firstname = forms.CharField(label='', widget=forms.TextInput({"placeholder": "First name"}))
    lastname = forms.CharField(label='', widget=forms.TextInput({"placeholder": "Last name"}))
    email = forms.CharField(label='', widget=forms.TextInput({"placeholder": "Email"}))
    phone = forms.CharField(label='', widget=forms.TextInput({"placeholder": "Phone number"}))


class RegisterForm(BaseRegisterForm):
    yubiid = forms.CharField(label='', widget=forms.HiddenInput)
    address = forms.CharField(label='', widget=forms.TextInput({"placeholder": "Address"}), required=False)
    city = forms.CharField(label='', widget=forms.TextInput({"placeholder": "City"}), required=False)
    state = forms.CharField(label='', widget=forms.TextInput({"placeholder": "State"}), required=False)
    zipcode = forms.CharField(label='', widget=forms.TextInput({"placeholder": "Zip code"}), required=False)
    password = forms.CharField(label='', widget=forms.PasswordInput)
    password2 = forms.CharField(label='', widget=forms.PasswordInput)

    def clean(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')

        if p1 and p2 and p1 != p2:
#			self._errors["password2"] = self.error_class(['Passwords don\'t match'])
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data


class DoctorRegisterForm(RegisterForm):
    speciality = forms.CharField(label='', widget=forms.TextInput({"placeholder": "Speciality"}),
                                 required=False)
    clinic = forms.CharField(label='', widget=forms.TextInput({"placeholder": "Clinic name"}), required=False)
    officemng_firstname = forms.CharField(label='',
                                          widget=forms.TextInput({"placeholder": "Office Manager First Name"}),
                                          required=False)
    officemng_lastname = forms.CharField(label='', widget=forms.TextInput({"placeholder": "Office Manager Last Name"}),
                                         required=False)
    officemng_email = forms.CharField(label='', widget=forms.TextInput({"placeholder": "Office Manager Email"}),
                                      required=False)
    website = forms.CharField(label='', widget=forms.TextInput({"placeholder": "Website"}), required=False)


class LoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()
    otp = forms.CharField(required=False)
    next = forms.CharField(widget=forms.HiddenInput, initial='/', required=False)


class FeedbackForm(forms.Form):
    email = forms.EmailField()
    text = forms.CharField()
    name = forms.CharField()
    phone = forms.CharField(required=False)
    daytime = forms.CharField()
    timezone = forms.CharField()
