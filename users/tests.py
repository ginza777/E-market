import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch
import pytest

User = get_user_model()


class UserModelTest(TestCase):
    """Test cases for User model functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '+1234567890',
            'password': 'testpass123'
        }
    
    def test_user_creation(self):
        """Test user creation with all fields."""
        user = User.objects.create_user(**self.user_data)
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.phone_number, '+1234567890')
        self.assertTrue(user.check_password('testpass123'))
        self.assertFalse(user.is_verified)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_user_string_representation(self):
        """Test user string representation."""
        user = User.objects.create_user(**self.user_data)
        expected = f"{user.first_name} {user.last_name} ({user.email})"
        self.assertEqual(str(user), expected)
    
    def test_user_email_unique(self):
        """Test that email must be unique."""
        User.objects.create_user(**self.user_data)
        
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='test@example.com',
                username='anotheruser',
                first_name='Another',
                last_name='User',
                password='testpass123'
            )
    
    def test_user_required_fields(self):
        """Test that required fields are enforced."""
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='test@example.com',
                username='testuser',
                # Missing first_name and last_name
                password='testpass123'
            )


class UserAPITest(APITestCase):
    """Test cases for User API endpoints."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '+1234567890',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        
        self.login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
    
    def test_user_registration_success(self):
        """Test successful user registration."""
        url = reverse('user-register')
        response = self.client.post(url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        
        user = User.objects.get(email='test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertFalse(user.is_verified)
    
    def test_user_registration_password_mismatch(self):
        """Test user registration with password mismatch."""
        self.user_data['password_confirm'] = 'differentpass'
        url = reverse('user-register')
        response = self.client.post(url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password_confirm', response.data)
        self.assertEqual(User.objects.count(), 0)
    
    def test_user_registration_weak_password(self):
        """Test user registration with weak password."""
        self.user_data['password'] = '123'
        self.user_data['password_confirm'] = '123'
        url = reverse('user-register')
        response = self.client.post(url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertEqual(User.objects.count(), 0)
    
    def test_user_registration_duplicate_email(self):
        """Test user registration with duplicate email."""
        User.objects.create_user(**{
            'email': 'test@example.com',
            'username': 'existinguser',
            'first_name': 'Existing',
            'last_name': 'User',
            'password': 'testpass123'
        })
        
        url = reverse('user-register')
        response = self.client.post(url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertEqual(User.objects.count(), 1)
    
    def test_user_login_success(self):
        """Test successful user login."""
        User.objects.create_user(**{
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123'
        })
        
        url = reverse('user-login')
        response = self.client.post(url, self.login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'test@example.com')
    
    def test_user_login_invalid_credentials(self):
        """Test user login with invalid credentials."""
        User.objects.create_user(**{
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123'
        })
        
        self.login_data['password'] = 'wrongpassword'
        url = reverse('user-login')
        response = self.client.post(url, self.login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
    
    def test_user_profile_authenticated(self):
        """Test user profile access with authentication."""
        user = User.objects.create_user(**{
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123'
        })
        
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        url = reverse('user-profile')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User')
    
    def test_user_profile_unauthenticated(self):
        """Test user profile access without authentication."""
        url = reverse('user-profile')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_token_refresh_success(self):
        """Test successful token refresh."""
        user = User.objects.create_user(**{
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123'
        })
        
        refresh = RefreshToken.for_user(user)
        
        url = reverse('token-refresh')
        response = self.client.post(url, {'refresh': str(refresh)}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_token_refresh_invalid(self):
        """Test token refresh with invalid token."""
        url = reverse('token-refresh')
        response = self.client.post(url, {'refresh': 'invalid_token'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


class UserIntegrationTest(APITestCase):
    """Integration tests for complete user flow."""
    
    def test_complete_user_flow(self):
        """Test complete user registration and login flow."""
        # Step 1: Register user
        registration_data = {
            'email': 'integration@example.com',
            'username': 'integrationuser',
            'first_name': 'Integration',
            'last_name': 'Test',
            'phone_number': '+1234567890',
            'password': 'integrationpass123',
            'password_confirm': 'integrationpass123'
        }
        
        register_url = reverse('user-register')
        response = self.client.post(register_url, registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Step 2: Login user
        login_data = {
            'email': 'integration@example.com',
            'password': 'integrationpass123'
        }
        
        login_url = reverse('user-login')
        response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        access_token = response.data['access']
        
        # Step 3: Access profile with token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        profile_url = reverse('user-profile')
        response = self.client.get(profile_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'integration@example.com')
        self.assertEqual(response.data['first_name'], 'Integration')
    
    def test_user_registration_signal(self):
        """Test that user registration triggers appropriate signals."""
        with patch('users.signals.user_registered.send') as mock_signal:
            registration_data = {
                'email': 'signal@example.com',
                'username': 'signaluser',
                'first_name': 'Signal',
                'last_name': 'Test',
                'password': 'signalpass123',
                'password_confirm': 'signalpass123'
            }
            
            register_url = reverse('user-register')
            response = self.client.post(register_url, registration_data, format='json')
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            # Note: Signal testing would require actual signal implementation


@pytest.mark.django_db
class UserPytestTest:
    """Pytest-based tests for User functionality."""
    
    def test_user_creation_with_pytest(self):
        """Test user creation using pytest."""
        user_data = {
            'email': 'pytest@example.com',
            'username': 'pytestuser',
            'first_name': 'Pytest',
            'last_name': 'Test',
            'password': 'pytestpass123'
        }
        
        user = User.objects.create_user(**user_data)
        assert user.email == 'pytest@example.com'
        assert user.username == 'pytestuser'
        assert user.first_name == 'Pytest'
        assert user.last_name == 'Test'
        assert user.check_password('pytestpass123')
        assert not user.is_verified
        assert user.is_active
    
    def test_user_email_validation(self):
        """Test email validation with pytest."""
        # Test valid email
        user = User.objects.create_user(
            email='valid@example.com',
            username='validuser',
            first_name='Valid',
            last_name='User',
            password='validpass123'
        )
        assert user.email == 'valid@example.com'
        
        # Test invalid email format
        with pytest.raises(Exception):
            User.objects.create_user(
                email='invalid-email',
                username='invaliduser',
                first_name='Invalid',
                last_name='User',
                password='invalidpass123'
            )
    
    def test_user_password_strength(self):
        """Test password strength validation."""
        # Test weak password
        with pytest.raises(Exception):
            User.objects.create_user(
                email='weak@example.com',
                username='weakuser',
                first_name='Weak',
                last_name='User',
                password='123'  # Too short
            )
        
        # Test strong password
        user = User.objects.create_user(
            email='strong@example.com',
            username='stronguser',
            first_name='Strong',
            last_name='User',
            password='StrongPass123!'
        )
        assert user.check_password('StrongPass123!')