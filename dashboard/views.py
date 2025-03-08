from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from .models import Profile
from django.contrib import messages


@login_required
def profile_view(request):
    instance, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been successfully updated!!!")
            return redirect("dashboard_profile")
        else:
            messages.error(request, "Failed to updated user profile!!!")
            return redirect("dashboard_profile")
    else:
        form = ProfileUpdateForm(instance=instance)
    template_name = "dashboard/profile.html"
    context = {"user": request.user, "form": form}
    return render(request, template_name=template_name, context=context)
