from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Cart, CartItem
from products.models import Product
import json

User = get_user_model()


@csrf_exempt
@require_http_methods(["POST"])
def add_to_cart(request):
    """Add product to cart."""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        if not product_id:
            return JsonResponse({
                'success': False,
                'message': 'Product ID is required'
            }, status=400)
        
        # Get or create cart for user
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            # For anonymous users, we'll use session-based cart
            # For now, return error for anonymous users
            return JsonResponse({
                'success': False,
                'message': 'Please login to add items to cart'
            }, status=401)
        
        # Get product
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Product not found'
            }, status=404)
        
        # Check stock availability
        if product.stock_quantity < quantity:
            return JsonResponse({
                'success': False,
                'message': f'Only {product.stock_quantity} items available in stock'
            }, status=400)
        
        # Add or update cart item
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({
            'success': True,
            'message': f'{product.title} added to cart',
            'cart_total_items': cart.total_items,
            'cart_total_price': cart.total_price
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Failed to add item to cart'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def update_cart_item(request):
    """Update cart item quantity."""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
        
        if not item_id:
            return JsonResponse({
                'success': False,
                'message': 'Item ID is required'
            }, status=400)
        
        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
            
            if quantity <= 0:
                cart_item.delete()
                return JsonResponse({
                    'success': True,
                    'message': 'Item removed from cart',
                    'cart_total_items': cart.total_items,
                    'cart_total_price': cart.total_price
                })
            
            # Check stock availability
            if cart_item.product.stock_quantity < quantity:
                return JsonResponse({
                    'success': False,
                    'message': f'Only {cart_item.product.stock_quantity} items available in stock'
                }, status=400)
            
            cart_item.quantity = quantity
            cart_item.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Cart updated',
                'cart_total_items': cart.total_items,
                'cart_total_price': cart.total_price,
                'item_total_price': cart_item.total_price
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Please login to update cart'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Failed to update cart'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def remove_from_cart(request):
    """Remove item from cart."""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        if not item_id:
            return JsonResponse({
                'success': False,
                'message': 'Item ID is required'
            }, status=400)
        
        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
            product_title = cart_item.product.title
            cart_item.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'{product_title} removed from cart',
                'cart_total_items': cart.total_items,
                'cart_total_price': cart.total_price
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Please login to remove items from cart'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Failed to remove item from cart'
        }, status=500)


@login_required
def cart_view(request):
    """Cart page view."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product').all()
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'frontend/cart.html', context)


@csrf_exempt
@require_http_methods(["GET"])
def get_cart_data(request):
    """Get cart data for AJAX requests."""
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = []
            for item in cart.items.select_related('product').all():
                cart_items.append({
                    'id': item.id,
                    'product_id': item.product.id,
                    'product_title': item.product.title,
                    'product_price': float(item.product.price),
                    'quantity': item.quantity,
                    'total_price': float(item.total_price),
                    'product_image': item.product.image.url if item.product.image else None
                })
            
            return JsonResponse({
                'success': True,
                'cart_total_items': cart.total_items,
                'cart_total_price': float(cart.total_price),
                'cart_items': cart_items
            })
        except Cart.DoesNotExist:
            return JsonResponse({
                'success': True,
                'cart_total_items': 0,
                'cart_total_price': 0.0,
                'cart_items': []
            })
    else:
        return JsonResponse({
            'success': True,
            'cart_total_items': 0,
            'cart_total_price': 0.0,
            'cart_items': []
        })
