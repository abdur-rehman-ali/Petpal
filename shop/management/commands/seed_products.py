from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random
from shop.models import Product
from django.utils.text import slugify

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with dummy pet product data"

    def handle(self, *args, **kwargs):
        # Get or create a test user
        user, created = User.objects.get_or_create(
            email="petseller@example.com",
            defaults={
                "email": "petseller@example.com",
                "username": "petSeller",
                "password": "petSeller123",
            },
        )

        self.stdout.write(self.style.SUCCESS(f"User: {user.email}, Created: {created}"))

        pet_product_types = [
            "Food",
            "Toy",
            "Bed",
            "Collar",
            "Leash",
            "Grooming",
            "Health",
            "Crate",
            "Litter",
            "Treat"
        ]

        pet_categories = [
            "Dog",
            "Cat",
            "Bird",
            "Fish",
            "Small Animal"
        ]

        products_list = []
        for _ in range(30):  # Creating 30 pet products
            product_type = random.choice(pet_product_types)
            pet_category = random.choice(pet_categories)
            
            # Generate appropriate product names and descriptions
            if product_type == "Food":
                name = f"{pet_category} {product_type} - {fake.word().title()} Formula"
                description = f"Premium {pet_category.lower()} {product_type.lower()} with {fake.word()} flavor. {fake.paragraph(nb_sentences=2)}"
            elif product_type == "Toy":
                name = f"{pet_category} {product_type} - {fake.word().title()} {random.choice(['Chew', 'Interactive', 'Plush'])}"
                description = f"Fun {pet_category.lower()} {product_type.lower()} for {random.choice(['puppies', 'kittens', 'adults', 'seniors'])}. {fake.paragraph(nb_sentences=2)}"
            else:
                name = f"{pet_category} {product_type} - {fake.word().title()} {product_type}"
                description = f"High-quality {pet_category.lower()} {product_type.lower()}. {fake.paragraph(nb_sentences=2)}"
            
            slug = slugify(name)
            
            products_list.append(
                {
                    "name": name,
                    "slug": slug,
                    "description": description,
                    "price": round(random.uniform(5.00, 100.00), 2),  # Pet products typically $5-$100
                    "stock": random.randint(5, 50),  # Reasonable stock levels
                    "is_available": random.choices([True, False], weights=[90, 10])[0],  # 90% chance available
                    "rating": round(random.uniform(3.0, 5.0), 2),  # Pet products usually well-rated
                    "seller": user,
                }
            )

        for product_data in products_list:
            self.stdout.write(self.style.SUCCESS(f"Seeding {product_data.get('name')}"))
            Product.objects.create(**product_data)
            
        self.stdout.write(self.style.SUCCESS("Pet products data seeded successfully!"))
