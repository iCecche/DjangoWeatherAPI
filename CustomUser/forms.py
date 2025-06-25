from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
        )  # new


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username"
        )  # new