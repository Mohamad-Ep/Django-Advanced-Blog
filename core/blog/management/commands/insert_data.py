from faker import Faker
from django.core.management.base import BaseCommand
from accounts.models import User, Profile
from ...models import Post, Category
import random

# __________________________________________________________

category_list = ["IT", "SPORT", "FUN", "DESGIN"]


class Command(BaseCommand):
    help = "Insert Dummy Data"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create(email=self.fake.email(), password="Aa123456@")
        profile = Profile.objects.get(user=user)
        profile.first_name = self.fake.first_name()
        profile.last_name = self.fake.last_name()
        profile.description = self.fake.paragraphs()
        profile.save()

        for name in category_list:
            Category.objects.get_or_create(name=name)

        for _ in range(3):
            Post.objects.create(
                title=self.fake.text(max_nb_chars=20),
                status=True,
                author=profile,
                category=Category.objects.get(name=random.choice(category_list)),
            )


# __________________________________________________________
