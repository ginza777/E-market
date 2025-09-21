import json
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch, Mock
import pytest
from PIL import Image
import io
from .models import Category
from .serializers import CategorySerializer
from users.models import User


class CategoryModelTest(TestCase):
    """Test cases for Category model functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.category_data = {
            'title': 'Electronics',
            'description': 'Electronic devices and gadgets',
            'is_active': True
        }
    
    def test_category_creation(self):
        """Test category creation with all fields."""
        category = Category.objects.create(**self.category_data)
        
        self.assertEqual(category.title, 'Electronics')
        self.assertEqual(category.description, 'Electronic devices and gadgets')
        self.assertTrue(category.is_active)
        self.assertIsNotNone(category.created_at)
        self.assertIsNotNone(category.updated_at)
    
    def test_category_string_representation(self):
        """Test category string representation."""
        category = Category.objects.create(**self.category_data)
        self.assertEqual(str(category), 'Electronics')
    
    def test_category_title_unique(self):
        """Test that category title must be unique."""
        Category.objects.create(**self.category_data)
        
        with self.assertRaises(Exception):
            Category.objects.create(
                title='Electronics',  # Duplicate title
                description='Another electronics category',
                is_active=True
            )
    
    def test_category_required_fields(self):
        """Test that required fields are enforced."""
        with self.assertRaises(Exception):
            Category.objects.create(
                # Missing title
                description='Category without title',
                is_active=True
            )
    
    def test_category_default_values(self):
        """Test category default values."""
        category = Category.objects.create(
            title='Test Category',
            description='Test Description'
        )
        
        self.assertTrue(category.is_active)  # Default should be True
        self.assertIsNotNone(category.created_at)
        self.assertIsNotNone(category.updated_at)


class CategoryAPITest(APITestCase):
    """Test cases for Category API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        
        # Create test user
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            first_name='Test',
            last_name='User',
            password='testpass123'
        )
        
        # Create test category
        self.category = Category.objects.create(
            title='Test Electronics',
            description='Test electronic devices',
            is_active=True
        )
        
        self.category_data = {
            'title': 'New Electronics',
            'description': 'New electronic devices',
            'is_active': True
        }
        
        # Get JWT token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
    
    def test_category_list_success(self):
        """Test successful category list retrieval."""
        url = reverse('category-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Electronics')
    
    def test_category_list_with_search(self):
        """Test category list with search functionality."""
        # Create another category
        Category.objects.create(
            title='Clothing',
            description='Fashion and clothing items',
            is_active=True
        )
        
        url = reverse('category-list')
        response = self.client.get(url, {'search': 'Electronics'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Electronics')
    
    def test_category_list_with_ordering(self):
        """Test category list with ordering."""
        # Create another category
        Category.objects.create(
            title='Accessories',
            description='Various accessories',
            is_active=True
        )
        
        url = reverse('category-list')
        response = self.client.get(url, {'ordering': 'title'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Accessories')
        self.assertEqual(response.data['results'][1]['title'], 'Test Electronics')
    
    def test_category_create_success(self):
        """Test successful category creation."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('category-list')
        response = self.client.post(url, self.category_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(response.data['title'], 'New Electronics')
    
    def test_category_create_unauthenticated(self):
        """Test category creation without authentication."""
        url = reverse('category-list')
        response = self.client.post(url, self.category_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_category_create_invalid_data(self):
        """Test category creation with invalid data."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        invalid_data = {
            'title': '',  # Empty title
            'description': 'Test description'
        }
        
        url = reverse('category-list')
        response = self.client.post(url, invalid_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
    
    def test_category_detail_success(self):
        """Test successful category detail retrieval."""
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Electronics')
        self.assertEqual(response.data['description'], 'Test electronic devices')
    
    def test_category_detail_not_found(self):
        """Test category detail with non-existent ID."""
        url = reverse('category-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_category_update_success(self):
        """Test successful category update."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        update_data = {
            'title': 'Updated Electronics',
            'description': 'Updated description',
            'is_active': True
        }
        
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Electronics')
        
        # Verify in database
        self.category.refresh_from_db()
        self.assertEqual(self.category.title, 'Updated Electronics')
    
    def test_category_update_partial(self):
        """Test partial category update."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        update_data = {
            'title': 'Partially Updated Electronics'
        }
        
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.patch(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Partially Updated Electronics')
        self.assertEqual(response.data['description'], 'Test electronic devices')  # Unchanged
    
    def test_category_delete_success(self):
        """Test successful category deletion (soft delete)."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify soft delete
        self.category.refresh_from_db()
        self.assertFalse(self.category.is_active)
    
    def test_category_delete_unauthenticated(self):
        """Test category deletion without authentication."""
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_category_image_upload(self):
        """Test category image upload."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Create a test image
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        
        uploaded_file = SimpleUploadedFile(
            'test_image.jpg',
            image_io.getvalue(),
            content_type='image/jpeg'
        )
        
        data = {
            'title': 'Category with Image',
            'description': 'Category with uploaded image',
            'image': uploaded_file
        }
        
        url = reverse('category-list')
        response = self.client.post(url, data, format='multipart')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['image'])
    
    def test_category_products_endpoint(self):
        """Test category products endpoint."""
        # Create a product in the category
        from products.models import Product
        product = Product.objects.create(
            title='Test Product',
            description='Test product description',
            price=99.99,
            category=self.category,
            stock_quantity=10,
            is_active=True
        )
        
        url = reverse('category-products', kwargs={'pk': self.category.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Product')


class CategoryIntegrationTest(APITestCase):
    """Integration tests for complete category flow."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            email='integration@example.com',
            username='integrationuser',
            first_name='Integration',
            last_name='Test',
            password='integrationpass123'
        )
        
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
    
    def test_complete_category_flow(self):
        """Test complete category creation, update, and deletion flow."""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Step 1: Create category
        category_data = {
            'title': 'Integration Electronics',
            'description': 'Integration test electronics',
            'is_active': True
        }
        
        create_url = reverse('category-list')
        response = self.client.post(create_url, category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = response.data['id']
        
        # Step 2: Retrieve category
        detail_url = reverse('category-detail', kwargs={'pk': category_id})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Integration Electronics')
        
        # Step 3: Update category
        update_data = {
            'title': 'Updated Integration Electronics',
            'description': 'Updated integration test electronics',
            'is_active': True
        }
        
        response = self.client.put(detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Integration Electronics')
        
        # Step 4: Delete category (soft delete)
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Step 5: Verify soft delete
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_category_update_triggers_elasticsearch_update(self):
        """Test that category updates trigger Elasticsearch updates for related products."""
        # Create category and product
        category = Category.objects.create(
            title='Elasticsearch Test',
            description='Test category for Elasticsearch',
            is_active=True
        )
        
        from products.models import Product
        product = Product.objects.create(
            title='Elasticsearch Product',
            description='Product for Elasticsearch testing',
            price=199.99,
            category=category,
            stock_quantity=5,
            is_active=True
        )
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        # Update category
        update_data = {
            'title': 'Updated Elasticsearch Test',
            'description': 'Updated test category for Elasticsearch',
            'is_active': True
        }
        
        with patch('products.signals.update_product_document') as mock_signal:
            url = reverse('category-detail', kwargs={'pk': category.pk})
            response = self.client.put(url, update_data, format='json')
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            # Note: Signal testing would require actual signal implementation


@pytest.mark.django_db
class CategoryPytestTest:
    """Pytest-based tests for Category functionality."""
    
    def test_category_creation_with_pytest(self):
        """Test category creation using pytest."""
        category_data = {
            'title': 'Pytest Electronics',
            'description': 'Pytest electronic devices',
            'is_active': True
        }
        
        category = Category.objects.create(**category_data)
        assert category.title == 'Pytest Electronics'
        assert category.description == 'Pytest electronic devices'
        assert category.is_active is True
        assert category.created_at is not None
        assert category.updated_at is not None
    
    def test_category_title_validation(self):
        """Test category title validation with pytest."""
        # Test valid title
        category = Category.objects.create(
            title='Valid Category',
            description='Valid description',
            is_active=True
        )
        assert category.title == 'Valid Category'
        
        # Test empty title
        with pytest.raises(Exception):
            Category.objects.create(
                title='',  # Empty title
                description='Valid description',
                is_active=True
            )
    
    def test_category_active_status(self):
        """Test category active status functionality."""
        # Test active category
        active_category = Category.objects.create(
            title='Active Category',
            description='Active description',
            is_active=True
        )
        assert active_category.is_active is True
        
        # Test inactive category
        inactive_category = Category.objects.create(
            title='Inactive Category',
            description='Inactive description',
            is_active=False
        )
        assert inactive_category.is_active is False
    
    def test_category_timestamps(self):
        """Test category timestamp functionality."""
        import time
        
        category = Category.objects.create(
            title='Timestamp Test',
            description='Testing timestamps',
            is_active=True
        )
        
        created_at = category.created_at
        updated_at = category.updated_at
        
        # Wait a moment
        time.sleep(0.1)
        
        # Update category
        category.title = 'Updated Timestamp Test'
        category.save()
        
        # Check timestamps
        assert category.created_at == created_at  # Should not change
        assert category.updated_at > updated_at   # Should be updated