from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random
from petlisting.models import Pet

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with dummy pet data"

    def handle(self, *args, **kwargs):
        user, created = User.objects.get_or_create(
            email="testuser@example.com",
            defaults={
                "email": "testuser@example.com",
                "username": "testUser",
                "password": "testUser123",
            },
        )

        self.stdout.write(self.style.SUCCESS(f"User: {user.email}, Created: {created}"))

        pets_list = []
        for _ in range(10):
            pets_list.append(
                {
                    "name": fake.first_name(),
                    "pet_type": random.choice(["dog", "cat", "bird", "fish", "other"]),
                    "breed": fake.word(),
                    "age": random.randint(1, 10),
                    "gender": random.choice(["male", "female"]),
                    "price": round(random.uniform(10.00, 1000.00), 2),
                    "description": fake.sentence(),
                    "location": fake.city(),
                    "status": random.choice(["available", "sold"]),
                }
            )

        for pet_data in pets_list:
            self.stdout.write(self.style.SUCCESS(f"Seeding {pet_data.get('name')}"))
            Pet.objects.create(seller=user, **pet_data)
        self.stdout.write(self.style.SUCCESS("Pets data seeded successfully..."))
