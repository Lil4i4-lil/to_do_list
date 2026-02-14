from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from .forms import ProfileForm


class ProfileUpdateView(UpdateView):
    model = get_user_model()
    form_class = ProfileForm
    template_name = "user_profile/profile.html"
    success_url = reverse_lazy("user_profile:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if "save" in request.POST:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        elif "cancel" in request.POST:
            return redirect("homepage:index")
        return redirect("homepage:index")


class ProfileCreateView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('homepage:index')

    def form_valid(self, form):
        response = super().form_valid(form)

        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)

        return response