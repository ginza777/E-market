from django.core.management.base import BaseCommand
from products.models import Product
from categories.models import Category
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Add images to existing products and categories'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing images before adding new ones',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing images...')
            # Clear existing images
            for product in Product.objects.all():
                if product.image:
                    product.image.delete(save=False)
                product.image = None
                product.save()
            
            for category in Category.objects.all():
                if category.image:
                    category.image.delete(save=False)
                category.image = None
                category.save()

        self.stdout.write('Adding images to products...')
        
        # Add images to products
        product_images = {
            'laptop': 'products/laptop.png',
            'textbook': 'products/textbook.png',
            'smart watch': 'products/smartwatch.png',
            'travel': 'products/travel.png',
            'sweater': 'products/sweater.png',
        }
        
        for product in Product.objects.all():
            # Find matching image based on title keywords
            image_path = None
            title_lower = product.title.lower()
            
            if 'laptop' in title_lower:
                image_path = product_images['laptop']
            elif 'textbook' in title_lower or 'book' in title_lower:
                image_path = product_images['textbook']
            elif 'watch' in title_lower or 'smart' in title_lower:
                image_path = product_images['smart watch']
            elif 'travel' in title_lower or 'guide' in title_lower:
                image_path = product_images['travel']
            elif 'sweater' in title_lower or 'clothing' in title_lower:
                image_path = product_images['sweater']
            else:
                # Default image for other products
                image_path = 'products/laptop.png'
            
            if image_path:
                full_path = os.path.join(settings.MEDIA_ROOT, image_path)
                if os.path.exists(full_path):
                    product.image = image_path
                    product.save()
                    self.stdout.write(f'Added image to product: {product.title}')
                else:
                    self.stdout.write(f'Image not found: {full_path}')
        
        self.stdout.write('Adding images to categories...')
        
        # Add images to categories
        category_images = {
            'technology': 'categories/technology.png',
            'books': 'categories/books.png',
            'fashion': 'categories/fashion.png',
        }
        
        for category in Category.objects.all():
            # Find matching image based on title keywords
            image_path = None
            title_lower = category.title.lower()
            
            if 'technology' in title_lower or 'tech' in title_lower:
                image_path = category_images['technology']
            elif 'book' in title_lower or 'education' in title_lower:
                image_path = category_images['books']
            elif 'fashion' in title_lower or 'clothing' in title_lower:
                image_path = category_images['fashion']
            else:
                # Default image for other categories
                image_path = 'categories/technology.png'
            
            if image_path:
                full_path = os.path.join(settings.MEDIA_ROOT, image_path)
                if os.path.exists(full_path):
                    category.image = image_path
                    category.save()
                    self.stdout.write(f'Added image to category: {category.title}')
                else:
                    self.stdout.write(f'Image not found: {full_path}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully added images to products and categories!')
        )
