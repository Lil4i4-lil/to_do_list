from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

from .forms import ProfileForm


def profile(request):
    profile_info = get_object_or_404(get_user_model(), id=request.user.id)
    form = ProfileForm(instance=profile_info)
    context = {'form': form}
    template = "user_profile/profile.html"
    return render(request, template, context)
