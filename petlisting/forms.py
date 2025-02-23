from django import forms
from .models import Pet


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            "name",
            "pet_type",
            "breed",
            "age",
            "gender",
            "price",
            "description",
            "location",
            "status",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }
