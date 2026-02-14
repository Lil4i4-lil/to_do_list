from django import forms
from django.contrib.auth import get_user_model

from .validators import validate_name


class ProfileForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        validators = {
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