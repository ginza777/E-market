from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    # Cart views
    path('', views.cart_view, name='cart'),
    
    # API endpoints
    path('api/add/', views.add_to_cart, name='add_to_cart'),
    path('api/update/', views.update_cart_item, name='update_cart_item'),
    path('api/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('api/data/', views.get_cart_data, name='get_cart_data'),
]
