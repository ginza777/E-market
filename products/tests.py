import json
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch, Mock
import pytest
from PIL import Image
import io
from .models import Product
from .serializers import ProductSerializer
from categories.models import Category
from users.models import User


class ProductModelTest(TestCase):
    """Test cases for Product model functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(
            title='Test Electronics',
            description='Test electronic devices',
            is_active=True
        )
        
        self.product_data = {
            'title': 'Test Product',
            'description': 'Test product description',
            'price': 99.99,
            'category': self.category,
            'stock_quantity': 10,
            'is_active': True
        }
    
    def test_product_creation(self):
        """Test product creation with all fields."""
        product = Product.objects.create(**self.product_data)
        
        self.assertEqual(product.title, 'Test Product')
        self.assertEqual(product.description, 'Test product description')
        self.assertEqual(product.price, 99.99)
        self.assertEqual(product.category, self.category)
        self.assertEqual(product.stock_quantity, 10)
        self.assertTrue(product.is_active)
        self.assertIsNotNone(product.created_at)
        self.assertIsNotNone(product.updated_at)
    
    def test_product_string_representation(self):
        """Test product string representation."""
        product = Product.objects.create(**self.product_data)
        self.assertEqual(str(product), 'Test Product')
    
    def test_product_category_relationship(self):
        """Test product category relationship."""
        product = Product.objects.create(**self.product_data)
        
        self.assertEqual(product.category.title, 'Test Electronics')
        self.assertEqual(product.category.description, 'Test electronic devices')
        
        # Test reverse relationship
        self.assertIn(product, self.category.products.all())
    
    def test_product_required_fields(self):
        """Test that required fields are enforced."""
        with self.assertRaises(Exception):
            Product.objects.create(
                # Missing title
                description='Product without title',
                price=99.99,
                category=self.category,
                stock_quantity=10
            )
    
    def test_product_price_validation(self):
        """Test product price validation."""
        # Test valid price
        product = Product.objects.create(**self.product_data)
        self.assertEqual(product.price, 99.99)
        
        # Test zero price
        product_zero = Product.objects.create(
            title='Zero Price Product',
            description='Product with zero price',
            price=0.00,
            category=self.category,
            stock_quantity=10
        )
        self.assertEqual(product_zero.price, 0.00)
    
    def test_product_stock_quantity(self):
        """Test product stock quantity functionality."""
        # Test positive stock
        product = Product.objects.create(**self.product_data)
        self.assertEqual(product.stock_quantity, 10)
        
        # Test zero stock
        product_zero = Product.objects.create(
            title='Zero Stock Product',
            description='Product with zero stock',
            price=99.99,
            category=self.category,
            stock_quantity=0
        )
        self.assertEqual(product_zero.stock_quantity, 0)
    
    def test_product_active_status(self):
        """Test product active status functionality."""
        # Test active product
        active_product = Product.objects.create(**self.product_data)
        self.assertTrue(active_product.is_active)
        
        # Test inactive product
        inactive_product = Product.objects.create(
            title='Inactive Product',
            description='Inactive product description',
            price=99.99,
            category=self.category,
            stock_quantity=10,
            is_active=False
        )
        self.assertFalse(inactive_product.is_active)


class ProductAPITest(APITestCase):
    """Test cases for Product API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        
        # Create test category
        self.category = Category.objects.create(
            title='Test Electronics',
            description='Test electronic devices',
            is_active=True
        )
        
        # Create test product
        self.product = Product.objects.create(
            title='Test Product',
            description='Test product description',
            price=99.99,
            category=self.category,
            stock_quantity=10,
            is_active=True
        )
        
        self.product_data = {
            'title': 'New Product',
            'description': 'New product description',
            'price': 199.99,
            'category': self.category.id,
            'stock_quantity': 20,
            'is_active': True
        }
        
        # Get JWT token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
    
    def test_product_list_success(self):
        """Test successful product list retrieval."""
        url = reverse('product-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Product')
    
    def test_product_list_with_search(self):
        """Test product list with search functionality."""
        # Create another product
        Product.objects.create(
            title='Another Product',
            description='Another product description',
            price=299.99,
            category=self.category,
            stock_quantity=5,
            is_active=True
        )
        
        url = reverse('product-list')
        response = self.client.get(url, {'search': 'Test'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Product')
    
    def test_product_list_with_category_filter(self):
        """Test product list with category filter."""
        # Create another category and product
        another_category = Category.objects.create(
            title='Another Category',
            description='Another category description',
            is_active=True
        )
        
        Product.objects.create(
            title='Another Category Product',
            description='Product in another category',
            price=399.99,
            category=another_category,
            stock_quantity=15,
            is_active=True
        )
        
        url = reverse('product-list')
        response = self.client.get(url, {'category': self.category.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Product')
    
    def test_product_list_with_ordering(self):
        """Test product list with ordering."""
        # Create another product
        Product.objects.create(
            title='A Product',
            description='Product starting with A',
            price=199.99,
            category=self.category,
            stock_quantity=5,
            is_active=True
        )
        
        url = reverse('product-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'A Product')
        self.assertEqual(response.data['results'][1]['title'], 'Test Product')
    
    def test_product_create_success(self):
        """Test successful product creation."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('product-list')
        response = self.client.post(url, self.product_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(response.data['title'], 'New Product')
    
    def test_product_create_unauthenticated(self):
        """Test product creation without authentication."""
        url = reverse('product-list')
        response = self.client.post(url, self.product_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_product_create_invalid_data(self):
        """Test product creation with invalid data."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        invalid_data = {
            'title': '',  # Empty title
            'description': 'Test description',
            'price': 'invalid_price',  # Invalid price
            'category': 999,  # Non-existent category
            'stock_quantity': -1  # Negative stock
        }
        
        url = reverse('product-list')
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
        self.assertIn('price', response.data)
        self.assertIn('category', response.data)
        self.assertIn('stock_quantity', response.data)
    
    def test_product_detail_success(self):
        """Test successful product detail retrieval."""
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Product')
        self.assertEqual(response.data['description'], 'Test product description')
        self.assertEqual(response.data['price'], '99.99')
    
    def test_product_detail_not_found(self):
        """Test product detail with non-existent ID."""
        url = reverse('product-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_product_update_success(self):
        """Test successful product update."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        update_data = {
            'title': 'Updated Product',
            'description': 'Updated description',
            'price': 149.99,
            'category': self.category.id,
            'stock_quantity': 15,
            'is_active': True
        }
        
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Product')
        self.assertEqual(response.data['price'], '149.99')
        
        # Verify in database
        self.product.refresh_from_db()
        self.assertEqual(self.product.title, 'Updated Product')
        self.assertEqual(self.product.price, 149.99)
    
    def test_product_update_partial(self):
        """Test partial product update."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        update_data = {
            'title': 'Partially Updated Product'
        }
        
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Partially Updated Product')
        self.assertEqual(response.data['description'], 'Test product description')  # Unchanged
    
    def test_product_delete_success(self):
        """Test successful product deletion (soft delete)."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify soft delete
        self.product.refresh_from_db()
        self.assertFalse(self.product.is_active)
    
    def test_product_delete_unauthenticated(self):
        """Test product deletion without authentication."""
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_product_image_upload(self):
        """Test product image upload."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Create a test image
        image = Image.new('RGB', (100, 100), color='blue')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        uploaded_file = SimpleUploadedFile(
            'test_product_image.jpg',
            image_io.getvalue(),
            content_type='image/jpeg'
        )
        
        data = {
            'title': 'Product with Image',
            'description': 'Product with uploaded image',
            'price': 299.99,
            'category': self.category.id,
            'stock_quantity': 10,
            'image': uploaded_file
        }
        
        url = reverse('product-list')
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['image'])
    
    def test_product_search_endpoint(self):
        """Test product search endpoint."""
        # Create more products for search testing
        Product.objects.create(
            title='iPhone 15',
            description='Latest iPhone model',
            price=999.99,
            category=self.category,
            stock_quantity=5,
            is_active=True
        )
        
        Product.objects.create(
            title='Samsung Galaxy',
            description='Samsung smartphone',
            price=899.99,
            category=self.category,
            stock_quantity=8,
            is_active=True
        )
        
        url = reverse('product-search')
        response = self.client.get(url, {'search': 'iPhone'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'iPhone 15')
    
    def test_product_low_stock_endpoint(self):
        """Test product low stock endpoint."""
        # Create products with different stock levels
        Product.objects.create(
            title='Low Stock Product 1',
            description='Product with low stock',
            price=199.99,
            category=self.category,
            stock_quantity=3,
            is_active=True
        )
        
        Product.objects.create(
            title='Low Stock Product 2',
            description='Another product with low stock',
            price=299.99,
            category=self.category,
            stock_quantity=7,
            is_active=True
        )
        
        Product.objects.create(
            title='High Stock Product',
            description='Product with high stock',
            price=399.99,
            category=self.category,
            stock_quantity=50,
            is_active=True
        )
        
        url = reverse('product-low-stock')
        response = self.client.get(url, {'threshold': 10})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)  # Original + 2 low stock products
    
    def test_product_price_range_filter(self):
        """Test product filtering by price range."""
        # Create products with different prices
        Product.objects.create(
            title='Cheap Product',
            description='Affordable product',
            price=49.99,
            category=self.category,
            stock_quantity=20,
            is_active=True
        )
        
        Product.objects.create(
            title='Expensive Product',
            description='Premium product',
            price=1999.99,
            category=self.category,
            stock_quantity=2,
            is_active=True
        )
        
        url = reverse('product-list')
        response = self.client.get(url, {'price__gte': 100, 'price__lte': 1000})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Only the original product


class ProductIntegrationTest(APITestCase):
    """Integration tests for complete product flow."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            email='integration@example.com',
            username='integrationuser',
            first_name='Integration',
            last_name='Test',
            password='integrationpass123'
        )
        
        self.category = Category.objects.create(
            title='Integration Electronics',
            description='Integration test electronics',
            is_active=True
        )
        
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
    
    def test_complete_product_flow(self):
        """Test complete product creation, update, and deletion flow."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Step 1: Create product
        product_data = {
            'title': 'Integration Product',
            'description': 'Integration test product',
            'price': 299.99,
            'category': self.category.id,
            'stock_quantity': 25,
            'is_active': True
        }
        
        create_url = reverse('product-list')
        response = self.client.post(create_url, product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product_id = response.data['id']
        
        # Step 2: Retrieve product
        detail_url = reverse('product-detail', kwargs={'pk': product_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Integration Product')
        
        # Step 3: Update product
        update_data = {
            'title': 'Updated Integration Product',
            'description': 'Updated integration test product',
            'price': 399.99,
            'category': self.category.id,
            'stock_quantity': 30,
            'is_active': True
        }
        
        response = self.client.put(detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Integration Product')
        self.assertEqual(response.data['price'], '399.99')
        
        # Step 4: Delete product (soft delete)
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Step 5: Verify soft delete
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_product_elasticsearch_integration(self):
        """Test product Elasticsearch integration."""
        # Create product
        product = Product.objects.create(
            title='Elasticsearch Product',
            description='Product for Elasticsearch testing',
            price=199.99,
            category=self.category,
            stock_quantity=5,
            is_active=True
        )
        
        # Test search functionality
        url = reverse('product-search')
        response = self.client.get(url, {'search': 'Elasticsearch'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Note: Actual Elasticsearch testing would require running Elasticsearch


@pytest.mark.django_db
class ProductPytestTest:
    """Pytest-based tests for Product functionality."""
    
    def test_product_creation_with_pytest(self):
        """Test product creation using pytest."""
        category = Category.objects.create(
            title='Pytest Electronics',
            description='Pytest electronic devices',
            is_active=True
        )
        
        product_data = {
            'title': 'Pytest Product',
            'description': 'Pytest product description',
            'price': 199.99,
            'category': category,
            'stock_quantity': 15,
            'is_active': True
        }
        
        product = Product.objects.create(**product_data)
        assert product.title == 'Pytest Product'
        assert product.description == 'Pytest product description'
        assert product.price == 199.99
        assert product.category == category
        assert product.stock_quantity == 15
        assert product.is_active is True
        assert product.created_at is not None
        assert product.updated_at is not None
    
    def test_product_price_validation(self):
        """Test product price validation with pytest."""
        category = Category.objects.create(
            title='Price Test Category',
            description='Category for price testing',
            is_active=True
        )
        
        # Test valid price
        product = Product.objects.create(
            title='Valid Price Product',
            description='Product with valid price',
            price=99.99,
            category=category,
            stock_quantity=10
        )
        assert product.price == 99.99
        
        # Test zero price
        zero_price_product = Product.objects.create(
            title='Zero Price Product',
            description='Product with zero price',
            price=0.00,
            category=category,
            stock_quantity=10
        )
        assert zero_price_product.price == 0.00
    
    def test_product_stock_management(self):
        """Test product stock management functionality."""
        category = Category.objects.create(
            title='Stock Test Category',
            description='Category for stock testing',
            is_active=True
        )
        
        # Test different stock levels
        products = [
            Product.objects.create(
                title=f'Stock Product {i}',
                description=f'Product with {i} stock',
                price=99.99,
                category=category,
                stock_quantity=i,
                is_active=True
            )
            for i in [0, 1, 5, 10, 100]
        ]
        
        # Test stock queries
        out_of_stock = Product.objects.filter(stock_quantity=0)
        low_stock = Product.objects.filter(stock_quantity__lte=5)
        high_stock = Product.objects.filter(stock_quantity__gte=10)
        
        assert len(out_of_stock) == 1
        assert len(low_stock) == 3  # 0, 1, 5
        assert len(high_stock) == 2  # 10, 100
    
    def test_product_category_relationship(self):
        """Test product-category relationship functionality."""
        category1 = Category.objects.create(
            title='Category 1',
            description='First category',
            is_active=True
        )
        
        category2 = Category.objects.create(
            title='Category 2',
            description='Second category',
            is_active=True
        )
        
        # Create products in different categories
        product1 = Product.objects.create(
            title='Product 1',
            description='Product in category 1',
            price=99.99,
            category=category1,
            stock_quantity=10
        )
        
        product2 = Product.objects.create(
            title='Product 2',
            description='Product in category 2',
            price=199.99,
            category=category2,
            stock_quantity=20
        )
        
        # Test relationships
        assert product1.category == category1
        assert product2.category == category2
        
        # Test reverse relationships
        assert product1 in category1.products.all()
        assert product2 in category2.products.all()
        assert product1 not in category2.products.all()
        assert product2 not in category1.products.all()
    
    def test_product_active_status(self):
        """Test product active status functionality."""
        category = Category.objects.create(
            title='Active Test Category',
            description='Category for active status testing',
            is_active=True
        )
        
        # Test active product
        active_product = Product.objects.create(
            title='Active Product',
            description='Active product description',
            price=99.99,
            category=category,
            stock_quantity=10,
            is_active=True
        )
        assert active_product.is_active is True
        
        # Test inactive product
        inactive_product = Product.objects.create(
            title='Inactive Product',
            description='Inactive product description',
            price=199.99,
            category=category,
            stock_quantity=5,
            is_active=False
        )
        assert inactive_product.is_active is False
        
        # Test filtering by active status
        active_products = Product.objects.filter(is_active=True)
        inactive_products = Product.objects.filter(is_active=False)
        
        assert len(active_products) == 1
        assert len(inactive_products) == 1
        assert active_product in active_products
        assert inactive_product in inactive_products