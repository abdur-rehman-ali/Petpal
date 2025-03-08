from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from .models import Profile
from django.contrib import messages


@login_required
def profile_view(request):
    instance, _ = Profile.objects.get_or_create(user=request.user)
    form = ProfileUpdateForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been successfully updated!!!")
            return redirect("dashboard_profile")
    template_name = "dashboard/profile.html"
    context = {"form": form}
    return render(request, template_name, context)
