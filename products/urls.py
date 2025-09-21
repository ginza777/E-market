from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductDocumentViewSet

router = DefaultRouter()
router.register(r'', ProductViewSet)
router.register(r'search', ProductDocumentViewSet, basename='product-search')

urlpatterns = [
    path('', include(router.urls)),
]
