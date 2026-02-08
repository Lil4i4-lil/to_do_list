from django import forms
from django.contrib.auth import get_user_model


class ProfileForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.split()[0]