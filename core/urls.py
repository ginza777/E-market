"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Django DRF E-commerce API",
        default_version='v1',
        description="""
        ## Comprehensive E-commerce API with Django REST Framework
        
        This API provides a complete e-commerce solution with the following features:
        
        ### 🔐 Authentication & Users
        - JWT-based authentication
        - User registration and login
        - User profile management
        - Token refresh functionality
        
        ### 📦 Products & Categories
        - CRUD operations for products and categories
        - Image upload support
        - Stock management
        - Category-based product filtering
        
        ### 🔍 Advanced Search
        - Elasticsearch-powered search
        - Full-text search across products
        - Advanced filtering and sorting
        - Real-time search suggestions
        
        ### 📊 Admin Panel
        - Comprehensive admin interface
        - Bulk operations
        - Analytics and reporting
        - Image previews and management
        
        ### 🐳 Docker Support
        - Complete containerization
        - PostgreSQL database
        - Elasticsearch integration
        - Kibana visualization
        
        ## Getting Started
        
        1. **Register a new user**: `POST /api/auth/register/`
        2. **Login**: `POST /api/auth/login/`
        3. **Browse products**: `GET /api/products/`
        4. **Search products**: `GET /api/products/search/`
        5. **Manage categories**: `GET /api/categories/`
        
        ## Authentication
        
        All protected endpoints require JWT authentication. Include the token in the Authorization header:
        ```
        Authorization: Bearer <your_access_token>
        ```
        
        ## Rate Limiting
        
        API requests are rate-limited to prevent abuse. Current limits:
        - 1000 requests per hour for authenticated users
        - 100 requests per hour for anonymous users
        
        ## Support
        
        For support and questions, please contact: support@example.com
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(
            name="API Support",
            email="support@example.com",
            url="https://example.com/support"
        ),
        license=openapi.License(
            name="MIT License",
            url="https://opensource.org/licenses/MIT"
        ),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    patterns=[
        path('api/', include('users.urls')),
        path('api/', include('categories.urls')),
        path('api/', include('products.urls')),
    ],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Frontend URLs
    path('', include('frontend.urls')),
    
    # API URLs
    path('api/auth/', include('users.urls')),
    path('api/categories/', include('categories.urls')),
    path('api/products/', include('products.urls')),
    path('api/cart/', include('cart.urls')),
    
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
