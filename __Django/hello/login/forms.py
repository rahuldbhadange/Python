from django import forms

class Registration_Form(forms.Form):
    first_Name = forms.CharField(max_length=20)
    last_Name = forms.CharField(max_length=20)
    email_ID = forms.EmailField()
