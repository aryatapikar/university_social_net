from django import forms
from django.core.exceptions import ValidationError

class EditProfileForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)
    semester = forms.CharField(max_length=10)
    section = forms.CharField(max_length=10)
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 10:
            raise ValidationError("Phone number must be 10 digits.")
        if not phone.isdigit():
            raise ValidationError("Phone number must only contain digits.")
        return phone
    
    def pass_match(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return password