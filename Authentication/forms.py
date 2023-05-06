from django.forms import ModelForm
from .models import User
from django import forms
from django.core.exceptions import ObjectDoesNotExist


class SignUpForm(ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            if myField != 'is_superuser':
                self.fields[myField].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'last_name', 'is_superuser')
        widgets = {
            'password': forms.PasswordInput(),
        }
        help_texts = {'username': None}

    def clean(self):
        # verify password confirmation match.
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        # checks if an email already exists or not
        email = self.cleaned_data.get('email')
        try:
            existing_user = User.objects.get(email__exact=email)
        except ObjectDoesNotExist:
            pass
        else:
            if existing_user.email == email:
                raise forms.ValidationError("Email already exists")

        # checking if username already exists
        username = self.cleaned_data.get('username')
        if len(username) <= 2:
            raise forms.ValidationError(
                "User name must be more than 2 characters")
        try:
            existing_user = User.objects.get(username__exact=username)
        except ObjectDoesNotExist:
            pass
        else:
            if existing_user.username == username:
                raise forms.ValidationError("Username already exists")


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        try:
            existing_user = User.objects.get(email__exact=email)
        except ObjectDoesNotExist:
            raise forms.ValidationError("Email or password does not match")
        else:
            if existing_user.email == email:
                pass

        if existing_user.check_password(password) or existing_user.password == password:
            pass
        else:
            raise forms.ValidationError("Email or password does not match")


class UpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            if myField != 'is_superuser':
                self.fields[myField].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'password')
        help_texts = {'username': None}

    def clean(self):
        password = self.cleaned_data.get("password")
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get('username')
        if not password:
            raise forms.ValidationError("Password cant be empty")
        if not username:
            raise forms.ValidationError("User name cant be empty")
        if not email:
            raise forms.ValidationError("Email Cant be Empty")

        try:
            existing_user = User.objects.get(username__exact=username)
        except ObjectDoesNotExist:
            raise forms.ValidationError("Sorry You cant change Username")
        else:
            pass
        if existing_user.email != email:
            try:
                User.objects.get(email__exact=email)
            except ObjectDoesNotExist:
                pass
            else:
                raise forms.ValidationError("Sorry You cant use this email")
