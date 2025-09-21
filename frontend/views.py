from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from products.models import Product
from categories.models import Category
import json


def home_view(request):
    """Home page view with search and product display."""
    # Get featured products (latest 8 products)
    featured_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    
    # Get active categories
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'featured_products': featured_products,
        'categories': categories,
    }
    return render(request, 'frontend/home.html', context)


def products_view(request):
    """Products page view with search and filtering."""
    products_list = Product.objects.filter(is_active=True).order_by('-created_at')
    categories = Category.objects.filter(is_active=True)

    # Search and Filter logic
    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    stock_status = request.GET.get('stock_status', '')
    order_by = request.GET.get('order_by', '-created_at')

    if search_query:
        products_list = products_list.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(category__title__icontains=search_query)
        )

    if category_filter:
        products_list = products_list.filter(category__id=category_filter)

    if min_price:
        products_list = products_list.filter(price__gte=min_price)

    if max_price:
        products_list = products_list.filter(price__lte=max_price)

    if stock_status:
        if stock_status == 'in_stock':
            products_list = products_list.filter(stock_quantity__gt=10)
        elif stock_status == 'low_stock':
            products_list = products_list.filter(stock_quantity__gt=0, stock_quantity__lte=10)
        elif stock_status == 'out_of_stock':
            products_list = products_list.filter(stock_quantity=0)

    products_list = products_list.order_by(order_by)

    # Pagination
    paginator = Paginator(products_list, 12)  # Show 12 products per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'category_filter': int(category_filter) if category_filter else '',
        'min_price': min_price,
        'max_price': max_price,
        'stock_status': stock_status,
        'order_by': order_by,
    }
    return render(request, 'frontend/products.html', context)


def categories_view(request):
    """Categories page view."""
    categories = Category.objects.filter(is_active=True).annotate(
        product_count=Count('product', filter=Q(product__is_active=True))
    ).order_by('title')
    
    # Get statistics
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    
    context = {
        'categories': categories,
        'total_products': total_products,
        'active_products': active_products,
    }
    return render(request, 'frontend/categories.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    """API login endpoint for frontend."""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return JsonResponse({
                'success': False,
                'message': 'Email and password are required'
            }, status=400)
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'is_verified': user.is_verified
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Account is disabled'
                }, status=400)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid email or password'
            }, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Login failed'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_register(request):
    """API register endpoint for frontend."""
    try:
        data = json.loads(request.body)
        
        required_fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password_confirm']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'success': False,
                    'message': f'{field.replace("_", " ").title()} is required'
                }, status=400)
        
        if data['password'] != data['password_confirm']:
            return JsonResponse({
                'success': False,
                'message': 'Passwords do not match'
            }, status=400)
        
        from users.models import User
        
        # Check if user already exists
        if User.objects.filter(email=data['email']).exists():
            return JsonResponse({
                'success': False,
                'message': 'A user with this email already exists'
            }, status=400)
        
        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({
                'success': False,
                'message': 'A user with this username already exists'
            }, status=400)
        
        # Create user
        user = User.objects.create_user(
            email=data['email'],
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=data['password']
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Registration successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_verified': user.is_verified
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Registration failed'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def api_logout(request):
    """API logout endpoint for frontend."""
    logout(request)
    return JsonResponse({
        'success': True,
        'message': 'Logout successful'
    })


@login_required
def api_profile(request):
    """API profile endpoint for frontend."""
    user = request.user
    return JsonResponse({
        'success': True,
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_verified': user.is_verified,
            'created_at': user.created_at.isoformat()
        }
    })


def api_check_auth(request):
    """Check if user is authenticated."""
    if request.user.is_authenticated:
        return JsonResponse({
            'authenticated': True,
            'user': {
                'id': request.user.id,
                'email': request.user.email,
                'username': request.user.username,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'is_verified': request.user.is_verified
            }
        })
    else:
        return JsonResponse({
            'authenticated': False
        })
