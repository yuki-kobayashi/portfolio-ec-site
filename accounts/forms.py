from django.contrib.auth.forms import AuthenticationForm
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
import re


CustomUser = get_user_model()


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, label="性")
    last_name = forms.CharField(max_length=30, label="名")
    address = forms.CharField(max_length=30, label="住所", required=False)
    tel = forms.CharField(max_length=30, label="電話番号", required=False)


class SignupUserForm(SignupForm):
    # オリジナルフォームのフィールド定義
    first_name = forms.CharField(max_length=30, label="性")
    last_name = forms.CharField(max_length=30, label="名")

    # メールアドレスの重複チェック
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("既に登録されているメールアドレスです。")
        return email
    
    # パスワードの入力制限
    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if not re.match(r"^[a-zA-Z0-9]+$", password):
            raise forms.ValidationError("パスワードは半角英数字のみで入力してください。")
        return password

    # 登録処理
    def save(self, request):
        user = super(SignupUserForm, self).save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user
    
class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': ("メールアドレスまたはパスワードが正しくありません。"),
    }
