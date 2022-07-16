from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    username = None

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name'
        )
