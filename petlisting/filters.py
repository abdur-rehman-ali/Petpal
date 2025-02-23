import django_filters
from .models import Pet


class PetFilter(django_filters.FilterSet):
    pet_type = django_filters.ChoiceFilter(choices=Pet.PET_TYPES, label="Type")
    gender = django_filters.ChoiceFilter(choices=Pet.GENDER_CHOICES, label="Gender")
    location = django_filters.CharFilter(lookup_expr="icontains", label="Location")
    status = django_filters.ChoiceFilter(choices=Pet.STATUS_CHOICES, label="Status")

    class Meta:
        model = Pet
        fields = [
            "pet_type",
            "gender",
            "location",
            "status",
        ]
