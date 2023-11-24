from django import forms
from django.core.exceptions import ValidationError

class SignupForm(forms.Form):
    name = forms.CharField(label='Full Name', max_length=100)
    student_id = forms.CharField(label='Student ID', max_length=100)
    phone = forms.CharField(label='Number', max_length=10)
    semester = forms.IntegerField(label='Semester')
    section = forms.CharField(label='Section', max_length=100)
    stud_teach = forms.ChoiceField(label='Student/Teacher', choices=[('student', 'Student'), ('teacher', 'Teacher')])
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
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