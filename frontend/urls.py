from django.urls import path
from . import views

app_name = 'frontend'

urlpatterns = [
    # Frontend pages
    path('', views.home_view, name='home'),
    path('products/', views.products_view, name='products'),
    path('categories/', views.categories_view, name='categories'),
    
    # API endpoints for frontend
    path('api/login/', views.api_login, name='api_login'),
    path('api/register/', views.api_register, name='api_register'),
    path('api/logout/', views.api_logout, name='api_logout'),
    path('api/profile/', views.api_profile, name='api_profile'),
    path('api/check-auth/', views.api_check_auth, name='api_check_auth'),
]
