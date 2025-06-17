from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, Product, UserProfile
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):  # ✅ This must be named exactly "Command"
    help = 'Seed the database with initial data'

    def handle(self, *args, **kwargs):
        # Create categories
        categories = ['Clothing', 'Electronics', 'Books', 'Furniture']
        for name in categories:
            Category.objects.get_or_create(name=name)

        # Create user and user profile
        user, created = User.objects.get_or_create(username='seller1')
        if created:
            user.set_password('test1234')
            user.save()

        if not hasattr(user, 'userprofile'):
            UserProfile.objects.create(user=user, is_seller=True)

        seller_profile = user.userprofile

        # Create products
        for _ in range(10):
            Product.objects.create(
                seller=seller_profile,
                name=fake.word().capitalize(),
                description=fake.text(max_nb_chars=100),
                price=random.randint(10, 500),
                category=Category.objects.order_by('?').first(),
                condition=random.choice(['new', 'used']),
                is_available=True
            )

        self.stdout.write(self.style.SUCCESS("✅ Successfully seeded the database."))
