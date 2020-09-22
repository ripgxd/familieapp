from django import forms


class AuthForm(forms.Form):
    username = forms.CharField(max_length=25, label='username')
    password = forms.CharField(widget=forms.PasswordInput(), label='password')

    username.widget.attrs.update({'class': 'form-control'})
    password.widget.attrs.update({'class': 'form-control'})
