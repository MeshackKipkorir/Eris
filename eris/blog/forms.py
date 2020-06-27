from django import forms
from django.contrib.auth.models import User
from .models import Profile

class CommentForm(forms.Form):
    author = forms.CharField(max_length = 100, widget = forms.TextInput(attrs = {
        "class" : "form-control",
        "placeholder":"Your Name"
    }))

    body = forms.CharField(widget = forms.Textarea(
        attrs={
            "class" : "form-control",
            "placeholder":"Leave a comment :-)"
        }
    ))

    email = forms.EmailField(widget = forms.TextInput(attrs = {
        "class":"form-control",
        "placeholder":"Your Email"
    }))

class EmailShareForm(forms.Form):
    name = forms.CharField(max_length = 25,widget = forms.TextInput(attrs = {
        "placeholder":"Your name...",
        "class":"form-control"
    }))
    email = forms.EmailField(widget = forms.TextInput(attrs = {
        "placeholder":"Recepients Address",
        "class":"form-control"
    }))
    to = forms.EmailField(widget = forms.TextInput(attrs = {
        "placeholder":"Recepients Address",
        "class":"form-control"
    }))
    comment = forms.CharField(required = False,widget = forms.Textarea(attrs = {
        "placeholder":"Leave a comment...",
        "class":"form-control"
    }))


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)
        
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label = 'password', widget = forms.PasswordInput)
    password2 = forms.CharField(label = 'Repeat Password', widget = forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username','first_name','email')

    def clean_password2(self):
        cd = self.cleaned_data

        if cd['password'] != cd['password2']:
            raise forms.ValidationError(' passwords do not match')

        return cd['password2']  

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio','photo')