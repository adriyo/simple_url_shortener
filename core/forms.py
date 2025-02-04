from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
        ]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email is invalid")
        return cleaned_data
