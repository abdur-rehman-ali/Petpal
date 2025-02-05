from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile_view(request):
    template_name = "dashboard/profile.html"
    context = {"user": request.user}
    return render(request, template_name=template_name, context=context)
