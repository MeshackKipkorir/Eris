from django import forms

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
        "placeholder":"Your name..."
    }))
    email = forms.EmailField()
    to = forms.EmailField(widget = forms.TextInput(attrs = {
        "placeholder":"Recepients Address"
    }))
    comment = forms.CharField(required = False,widget = forms.Textarea(attrs = {
        "placeholder":"Leave a comment..."
    }))