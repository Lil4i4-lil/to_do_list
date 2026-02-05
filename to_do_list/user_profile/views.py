from django.shortcuts import render


def profile(request):
    template = "user_profile/profile.html"
    return render(request, template)
