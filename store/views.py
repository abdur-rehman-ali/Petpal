from django.shortcuts import render
from .models import Store


def list_view(request):
    stores = Store.objects.all()
    context = {"stores": stores}
    template_name = "store/listing.html"
    return render(request, template_name, context)
