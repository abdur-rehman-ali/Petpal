from django import forms
from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "bio",
            "date_of_birth",
            "primary_contact_number",
            "secondary_contact_number",
            "address",
            "city",
            "country",
            "websiteURL",
            "gender",
            "occupation",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }
