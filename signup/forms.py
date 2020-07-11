from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    #icon = forms.ImageField(label = "アイコン", required = False)
    class Meta:
        model = User
        #fields = ("username", "icon")
        fields = ("username","email")

class CustomUserChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ("username", "icon", "email")


    # 入力後戻った時にパスワードも入力済みにする　
class CustomUpdateForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['is_active']
