# Generated by Django 5.1.4 on 2025-05-18 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("petlisting", "0002_pet_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="pet",
            name="contact_number",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
