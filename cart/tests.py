from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Product, Category
from .models import Cart, CartItem

User = get_user_model()


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            title='Test Category',
            description='Test Description'
        )
        self.product = Product.objects.create(
            title='Test Product',
            description='Test Description',
            price=100.00,
            category=self.category,
            stock_quantity=10
        )

    def test_cart_creation(self):
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
        self.assertEqual(cart.total_items, 0)
        self.assertEqual(cart.total_price, 0)

    def test_cart_item_creation(self):
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )
        self.assertEqual(cart_item.cart, cart)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.total_price, 200.00)

    def test_cart_total_items(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        # Create another product for the second item
        product2 = Product.objects.create(
            title='Test Product 2',
            description='Test Description 2',
            price=50.00,
            category=self.category,
            stock_quantity=5
        )
        CartItem.objects.create(cart=cart, product=product2, quantity=3)
        self.assertEqual(cart.total_items, 5)

    def test_cart_total_price(self):
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        self.assertEqual(cart.total_price, 200.00)


class CartAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            title='Test Category',
            description='Test Description'
        )
        self.product = Product.objects.create(
            title='Test Product',
            description='Test Description',
            price=100.00,
            category=self.category,
            stock_quantity=10
        )

    def test_add_to_cart_unauthenticated(self):
        url = reverse('cart:add_to_cart')
        data = {'product_id': self.product.id, 'quantity': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_to_cart_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('cart:add_to_cart')
        data = {'product_id': self.product.id, 'quantity': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['cart_total_items'], 2)

    def test_add_to_cart_insufficient_stock(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('cart:add_to_cart')
        data = {'product_id': self.product.id, 'quantity': 15}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

    def test_update_cart_item(self):
        self.client.force_authenticate(user=self.user)
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )
        
        url = reverse('cart:update_cart_item')
        data = {'item_id': cart_item.id, 'quantity': 5}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['cart_total_items'], 5)

    def test_remove_from_cart(self):
        self.client.force_authenticate(user=self.user)
        cart = Cart.objects.create(user=self.user)
        cart_item = CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )
        
        url = reverse('cart:remove_from_cart')
        data = {'item_id': cart_item.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertEqual(response.data['cart_total_items'], 0)

    def test_get_cart_data(self):
        self.client.force_authenticate(user=self.user)
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=2
        )
        
        url = reverse('cart:get_cart_data')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['success'])
        self.assertEqual(response.json()['cart_total_items'], 2)
        self.assertEqual(len(response.json()['cart_items']), 1)
