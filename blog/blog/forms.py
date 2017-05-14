from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout,get_user_model

from .models import Post


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','text',)


User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self,*args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username,password=password)
            if not user:
                raise forms.ValidationError("This user does not exist")

            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")

            if not user.is_active:
                raise forms.ValidationError("This user is no longer active ")

            return super(UserLoginForm,self).clean(*args,**kwargs)

class SignUpForm(forms.ModelForm):
    username = forms.CharField(max_length=30,required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput,required=True)
    email = forms.CharField(widget=forms.EmailInput,required=True,max_length=75)

    class Meta:
        model = User
        fields = ['username','email','password','confirm_password']

    def clean(self):
        super(SignUpForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and password != confirm_password:
            self._errors['password'] = self.error_class(
                ['Passwords don\'t match'])
        return self.cleaned_data
