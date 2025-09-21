from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from categories.models import Category
from products.models import Product
from decimal import Decimal
import random
from faker import Faker

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = 'Create fake data for testing and development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create'
        )
        parser.add_argument(
            '--categories',
            type=int,
            default=5,
            help='Number of categories to create'
        )
        parser.add_argument(
            '--products',
            type=int,
            default=50,
            help='Number of products to create'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Product.objects.all().delete()
            Category.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared'))

        # Create users
        self.create_users(options['users'])
        
        # Create categories
        categories = self.create_categories(options['categories'])
        
        # Create products
        self.create_products(options['products'], categories)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {options["users"]} users, '
                f'{options["categories"]} categories, and '
                f'{options["products"]} products'
            )
        )

    def create_users(self, count):
        """Create fake users"""
        self.stdout.write(f'Creating {count} users...')
        
        for _ in range(count):
            User.objects.create_user(
                email=fake.email(),
                username=fake.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number()[:15],
                password='testpass123',
                is_verified=random.choice([True, False])
            )

    def create_categories(self, count):
        """Create fake categories"""
        self.stdout.write(f'Creating {count} categories...')
        
        categories = []
        category_names = [
            'Electronics', 'Books', 'Clothing', 'Home & Garden',
            'Sports', 'Beauty', 'Toys', 'Automotive', 'Health',
            'Food & Beverages', 'Jewelry', 'Furniture'
        ]
        
        for i in range(count):
            name = category_names[i] if i < len(category_names) else fake.word().title()
            category = Category.objects.create(
                title=name,
                description=fake.text(max_nb_chars=200),
                is_active=random.choice([True, False])
            )
            categories.append(category)
        
        return categories

    def create_products(self, count, categories):
        """Create fake products"""
        self.stdout.write(f'Creating {count} products...')
        
        product_templates = {
            'Electronics': [
                'Smartphone', 'Laptop', 'Tablet', 'Headphones', 'Speaker',
                'Camera', 'Smart Watch', 'Gaming Console', 'TV', 'Monitor'
            ],
            'Books': [
                'Novel', 'Textbook', 'Biography', 'Cookbook', 'Travel Guide',
                'Science Fiction', 'Mystery', 'Romance', 'History', 'Poetry'
            ],
            'Clothing': [
                'T-Shirt', 'Jeans', 'Dress', 'Jacket', 'Sweater',
                'Shoes', 'Hat', 'Scarf', 'Belt', 'Sunglasses'
            ],
            'Home & Garden': [
                'Plant Pot', 'Garden Tool', 'Decorative Item', 'Light Fixture',
                'Kitchen Appliance', 'Furniture', 'Rug', 'Curtain', 'Mirror'
            ],
            'Sports': [
                'Running Shoes', 'Tennis Racket', 'Basketball', 'Yoga Mat',
                'Dumbbells', 'Bicycle', 'Swimming Goggles', 'Golf Club'
            ]
        }
        
        for _ in range(count):
            category = random.choice(categories)
            category_name = category.title
            
            # Get appropriate product name based on category
            if category_name in product_templates:
                base_name = random.choice(product_templates[category_name])
                product_name = f"{base_name} {fake.word().title()}"
            else:
                product_name = f"{fake.word().title()} {fake.word().title()}"
            
            Product.objects.create(
                title=product_name,
                description=fake.text(max_nb_chars=500),
                price=Decimal(str(round(random.uniform(10, 2000), 2))),
                category=category,
                stock_quantity=random.randint(0, 100),
                is_active=random.choice([True, False])
            )
