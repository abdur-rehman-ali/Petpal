from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from store.models import Store

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with dummy store data"

    def handle(self, *args, **kwargs):
        user, created = User.objects.get_or_create(
            email="teststoreowner@example.com",
            defaults={
                "email": "teststoreowner@example.com",
                "username": "testOwner",
                "password": "testOwner123",
            },
        )

        self.stdout.write(self.style.SUCCESS(f"User: {user.email}, Created: {created}"))

        for _ in range(10):
            store = Store.objects.create(
                name=fake.company(),
                description=fake.sentence(),
                email=fake.email(),
                phone=fake.phone_number(),
                address=fake.address(),
                website=fake.url(),
                facebook=fake.url(),
                instagram=fake.url(),
                twitter=fake.url(),
                owner=user,
            )

            self.stdout.write(self.style.SUCCESS(f"Seeded Store: {store.name}"))
        self.stdout.write(self.style.SUCCESS("Store data seeded successfully!"))
