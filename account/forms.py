from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=250)
    email = forms.EmailField(max_length=250)
    password = forms.CharField(max_length=250)
    password2 = forms.CharField(max_length=250)


    class Meta:
        model = User
        fields = ('username','email')


    error_message = {
        'password mismatch': 'Two password field didn\' match'
    }
    def clean_password_2(self):
        password = self.cleaned_data["password"]
        password2 = self.cleaned_data["password2"]

        if password and password2 and password != password2:
            raise ValidationError(
                self.error_message,
                code = 'password_mismatch'
            )
        
        return password2


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
    
