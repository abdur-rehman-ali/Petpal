import os
import requests
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random
import cloudinary.uploader
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

        pet_images = {
            "cat": [
                "https://cdn.pixabay.com/photo/2017/02/20/18/03/cat-2083492_1280.jpg",
                "https://cdn.pixabay.com/photo/2014/11/30/14/11/cat-551554_1280.jpg",
                "https://cdn.pixabay.com/photo/2015/11/16/14/43/cat-1045782_1280.jpg",
                "https://cdn.pixabay.com/photo/2017/11/14/13/06/kitty-2948404_1280.jpg",
                "https://cdn.pixabay.com/photo/2018/01/28/12/37/cat-3113513_1280.jpg",
            ],
            "dog": [
                "https://cdn.pixabay.com/photo/2016/12/13/05/15/puppy-1903313_1280.jpg",
                "https://cdn.pixabay.com/photo/2019/08/19/07/45/dog-4415649_1280.jpg",
                "https://cdn.pixabay.com/photo/2017/09/25/13/12/dog-2785074_1280.jpg",
                "https://cdn.pixabay.com/photo/2016/02/19/15/46/dog-1210559_1280.jpg",
                "https://cdn.pixabay.com/photo/2015/11/17/13/13/dog-1047518_1280.jpg",
            ],
            "bird": [
                "https://cdn.pixabay.com/photo/2017/02/07/16/47/kingfisher-2046453_1280.jpg",
                "https://cdn.pixabay.com/photo/2018/08/12/16/59/parrot-3601194_1280.jpg",
                "https://cdn.pixabay.com/photo/2017/03/13/10/25/hummingbird-2139279_1280.jpg",
                "https://cdn.pixabay.com/photo/2016/11/14/04/45/elephant-bird-1822636_1280.jpg",
                "https://cdn.pixabay.com/photo/2017/03/27/14/33/animal-2178668_1280.jpg",
            ],
            "fish": [
                "https://cdn.pixabay.com/photo/2016/12/31/21/22/discus-fish-1943755_1280.jpg",
                "https://cdn.pixabay.com/photo/2017/01/31/16/36/background-2025788_1280.jpg",
                "https://cdn.pixabay.com/photo/2016/03/05/19/37/fish-1238248_1280.jpg",
                "https://cdn.pixabay.com/photo/2016/12/31/21/22/discus-fish-1943755_1280.jpg",
                "https://cdn.pixabay.com/photo/2017/01/31/16/36/background-2025788_1280.jpg",
            ],
            "other": [
                "https://cdn.pixabay.com/photo/2017/05/31/18/38/sea-2361247_1280.jpg",  # Turtle
                "https://cdn.pixabay.com/photo/2017/10/20/10/58/elephant-2870777_1280.jpg",  # Elephant
                "https://cdn.pixabay.com/photo/2017/01/14/12/59/iceland-1979445_1280.jpg",  # Horse
                "https://cdn.pixabay.com/photo/2017/05/08/13/15/spring-bok-2295434_1280.jpg",  # Springbok
                "https://cdn.pixabay.com/photo/2017/01/16/19/54/ireland-1985088_1280.jpg",  # Sheep
            ],
        }

        temp_dir = "temp_images"
        os.makedirs(temp_dir, exist_ok=True)

        pets_list = []
        for _ in range(10):
            pet_type = random.choice(["cat", "dog", "bird", "fish", "other"])
            image_url = random.choice(pet_images[pet_type])

            # Download the image
            response = requests.get(image_url)
            if response.status_code == 200:
                image_name = os.path.join(temp_dir, f"{pet_type}_{fake.uuid4()}.jpg")
                with open(image_name, "wb") as f:
                    f.write(response.content)

                upload_result = cloudinary.uploader.upload(image_name)
                os.remove(image_name)

                pets_list.append(
                    {
                        "name": fake.first_name(),
                        "pet_type": pet_type,
                        "breed": fake.word(),
                        "age": random.randint(1, 10),
                        "gender": random.choice(["male", "female"]),
                        "price": round(random.uniform(10.00, 1000.00), 2),
                        "description": fake.sentence(),
                        "location": fake.city(),
                        "status": random.choice(["available", "sold"]),
                        "image": upload_result["public_id"],
                    }
                )
            else:
                self.stdout.write(self.style.ERROR(f"Failed to download image: {image_url}"))

        for pet_data in pets_list:
            self.stdout.write(self.style.SUCCESS(f"Seeding {pet_data.get('name')}"))
            Pet.objects.create(seller=user, **pet_data)
        self.stdout.write(self.style.SUCCESS("Pets data seeded successfully..."))
