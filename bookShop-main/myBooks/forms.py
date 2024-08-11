from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import myUser
class MyRegFrm(UserCreationForm):
    username =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username'}))
    first_name =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    email =forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    mobile =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Mobile'}))
    password1 =forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

    password2 =forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))

    
    class Meta:
        model=myUser
        fields=["username","first_name",'last_name','email','mobile']
class LoginFrm(AuthenticationForm):
        username =forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username','id':'username1'}))
        password =forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'cols':'70'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'cols':'70'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'cols':'70','rows':'3'}))        


