from django import forms


class PhoneLoginForm(forms.Form):
    phoneNumber = forms.CharField(max_length=20)

class PhoneVerifyForm(forms.Form):
    otp = forms.IntegerField()