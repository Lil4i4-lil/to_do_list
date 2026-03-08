from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .validators import validate_name

BIRTH_YEAR_CHOICES = list(map(str, range(1926, 2026)))

class ProfileForm(forms.ModelForm):
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        required=False,
        input_formats=['%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y']
    )

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'phone_number',
            'first_name',
            'last_name',
            'birthday'
        )
        validators = { # noqa: RUF012
            'first_name': (validate_name,),
            'last_name': (validate_name,),
        }

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '')

        if first_name:
            validate_name(first_name)

            return first_name.split()[0]
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '')

        if last_name:
            validate_name(last_name)

        return last_name


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()  # Ваша кастомная модель
        fields = ('username', 'email')