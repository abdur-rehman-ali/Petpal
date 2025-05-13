import os
import requests
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random
import cloudinary.uploader
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

        # Verified working product images organized by type
        product_images = {
            "Food": [
                "https://images.unsplash.com/photo-1589927986089-35812388d1f4",  # Dog food
                "https://images.unsplash.com/photo-1568640347023-a616a30bc3bd",  # Cat food
                "https://images.unsplash.com/photo-1621876111750-1a6b0f5d1e1f",  # Bird food
                "https://images.unsplash.com/photo-1551290464-66719418ca54",  # Fish food
                "https://images.unsplash.com/photo-1632338948272-1eaf9a6a6c8a",  # Pet treats
            ],
            "Toy": [
                "https://images.unsplash.com/photo-1586671267731-da2cf3ceeb80",  # Dog toy
                "https://images.unsplash.com/photo-1591769225440-811ad7d6eab2",  # Cat toy
                "https://images.unsplash.com/photo-1551298370-9d3d53740c72",  # Chew toy
                "https://images.unsplash.com/photo-1551298370-9d3d53740c72",  # Plush toy
                "https://images.unsplash.com/photo-1551298370-9d3d53740c72",  # Interactive toy
            ],
            "Bed": [
                "https://images.unsplash.com/photo-1594149929911-78975a43d4f5",  # Dog bed
                "https://images.unsplash.com/photo-1594149929911-78975a43d4f5",  # Cat bed
                "https://images.unsplash.com/photo-1594149929911-78975a43d4f5",  # Pet bed
                "https://images.unsplash.com/photo-1594149929911-78975a43d4f5",  # Cozy bed
                "https://images.unsplash.com/photo-1594149929911-78975a43d4f5",  # Luxury bed
            ],
            "Collar": [
                "https://images.unsplash.com/photo-1588943211346-0908a1fb0b01",  # Dog collar
                "https://images.unsplash.com/photo-1588943211346-0908a1fb0b01",  # Cat collar
                "https://images.unsplash.com/photo-1588943211346-0908a1fb0b01",  # Leather collar
                "https://images.unsplash.com/photo-1588943211346-0908a1fb0b01",  # Patterned collar
                "https://images.unsplash.com/photo-1588943211346-0908a1fb0b01",  # Designer collar
            ],
            "Other": [
                "https://images.unsplash.com/photo-1551298370-9d3d53740c72",  # Pet carrier
                "https://images.unsplash.com/photo-1551298370-9d3d53740c72",  # Litter box
                "https://images.unsplash.com/photo-1551298370-9d3d53740c72",  # Grooming kit
                "https://images.unsplash.com/photo-1551298370-9d3d53740c72",  # Pet bowl
                "https://images.unsplash.com/photo-1551298370-9d3d53740c72",  # Health supplies
            ]
        }

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

        temp_dir = "temp_product_images"
        os.makedirs(temp_dir, exist_ok=True)

        products_list = []
        for _ in range(4):  # Creating 30 pet products
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
            
            # Get an appropriate image for the product type
            image_type = product_type if product_type in product_images else "Other"
            image_url = random.choice(product_images[image_type])

            try:
                # Download and upload the image
                response = requests.get(image_url)
                response.raise_for_status()  # Raise exception for bad status codes
                
                image_name = os.path.join(temp_dir, f"{slug}_{fake.uuid4()}.jpg")
                with open(image_name, "wb") as f:
                    f.write(response.content)

                upload_result = cloudinary.uploader.upload(image_name)
                os.remove(image_name)
                print(f"Uploaded image for {name}: {upload_result['url']}")

                products_list.append(
                    {
                        "name": name,
                        "slug": slug,
                        "description": description,
                        "price": round(random.uniform(5.00, 100.00), 2),
                        "stock": random.randint(5, 50),
                        "is_available": random.choices([True, False], weights=[90, 10])[0],
                        "rating": round(random.uniform(3.0, 5.0), 2),
                        "seller": user,
                        "image": upload_result["public_id"],
                    }
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Failed to process image for {name}: {str(e)}")
                )
                continue

        for product_data in products_list:
            try:
                self.stdout.write(self.style.SUCCESS(f"Seeding {product_data.get('name')}"))
                Product.objects.create(**product_data)
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Failed to create product {product_data.get('name')}: {str(e)}")
                )
            
        self.stdout.write(self.style.SUCCESS("Pet products data seeded successfully!"))
