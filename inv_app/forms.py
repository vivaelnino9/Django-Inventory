from django import forms
from inv_app.models import User, Inv_User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class Inv_UserForm(forms.ModelForm):
    class Meta:
        model = Inv_User
        fields = ('first_name', 'last_name')