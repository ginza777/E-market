from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from .models import Category
from .serializers import CategorySerializer


class CategoryListView(generics.ListCreateAPIView):
    """
    Category list and create endpoint.
    
    GET: List all active categories
    POST: Create new category (Admin only)
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]
    
    @swagger_auto_schema(
        operation_summary="List all categories",
        operation_description="""
        Get a list of all active categories.
        
        **Features:**
        - Returns only active categories
        - Includes product count for each category
        - Supports pagination
        - No authentication required
        
        **Response Codes:**
        - **200 OK**: Categories retrieved successfully
        - **500 Internal Server Error**: Server error
        """,
        responses={
            200: openapi.Response(
                description="✅ Categories retrieved successfully",
                examples={
                    "application/json": {
                        "count": 3,
                        "next": None,
                        "previous": None,
                        "results": [
                            {
                                "id": 1,
                                "title": "Electronics",
                                "description": "Electronic devices and gadgets",
                                "image": "http://127.0.0.1:8001/media/categories/electronics.jpg",
                                "is_active": True,
                                "created_at": "2024-01-15T10:30:00Z",
                                "updated_at": "2024-01-15T10:30:00Z",
                                "product_count": 15
                            },
                            {
                                "id": 2,
                                "title": "Books",
                                "description": "Books and educational materials",
                                "image": "http://127.0.0.1:8001/media/categories/books.jpg",
                                "is_active": True,
                                "created_at": "2024-01-15T10:30:00Z",
                                "updated_at": "2024-01-15T10:30:00Z",
                                "product_count": 8
                            }
                        ]
                    }
                }
            ),
            500: openapi.Response(
                description="❌ Internal server error",
                examples={
                    "application/json": {
                        "detail": "Internal server error occurred"
                    }
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Create new category",
        operation_description="""
        Create a new category (Admin only).
        
        **Request Body:**
        ```json
        {
            "title": "New Category",
            "description": "Category description",
            "image": "image_file.jpg",
            "is_active": true
        }
        ```
        
        **Authentication Required:**
        - Admin user only
        - Include JWT token in Authorization header
        - Format: `Bearer <access_token>`
        
        **Response Codes:**
        - **201 Created**: Category created successfully
        - **400 Bad Request**: Validation errors
        - **401 Unauthorized**: Authentication required
        - **403 Forbidden**: Admin access required
        - **500 Internal Server Error**: Server error
        """,
        request_body=CategorySerializer,
        responses={
            201: openapi.Response(
                description="✅ Category created successfully",
                schema=CategorySerializer,
                examples={
                    "application/json": {
                        "id": 3,
                        "title": "New Category",
                        "description": "Category description",
                        "image": "http://127.0.0.1:8001/media/categories/new_category.jpg",
                        "is_active": True,
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-15T10:30:00Z"
                    }
                }
            ),
            400: openapi.Response(
                description="❌ Validation errors",
                examples={
                    "application/json": {
                        "title": ["This field is required."],
                        "description": ["This field is required."],
                        "image": ["The submitted file is empty."]
                    }
                }
            ),
            401: openapi.Response(
                description="❌ Authentication required",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
            403: openapi.Response(
                description="❌ Admin access required",
                examples={
                    "application/json": {
                        "detail": "You do not have permission to perform this action."
                    }
                }
            ),
            500: openapi.Response(
                description="❌ Internal server error",
                examples={
                    "application/json": {
                        "detail": "Internal server error occurred"
                    }
                }
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Category detail endpoint.
    
    GET: Get category details
    PUT: Update category (Admin only)
    DELETE: Delete category (Admin only)
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]
    
    @swagger_auto_schema(
        operation_summary="Get category details",
        operation_description="""
        Get detailed information about a specific category.
        
        **Features:**
        - Returns category details including product count
        - No authentication required
        - Includes related products information
        
        **Response Codes:**
        - **200 OK**: Category details retrieved successfully
        - **404 Not Found**: Category not found
        - **500 Internal Server Error**: Server error
        """,
        responses={
            200: openapi.Response(
                description="✅ Category details retrieved successfully",
                schema=CategorySerializer,
                examples={
                    "application/json": {
                        "id": 1,
                        "title": "Electronics",
                        "description": "Electronic devices and gadgets",
                        "image": "http://127.0.0.1:8001/media/categories/electronics.jpg",
                        "is_active": True,
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-15T10:30:00Z",
                        "product_count": 15
                    }
                }
            ),
            404: openapi.Response(
                description="❌ Category not found",
                examples={
                    "application/json": {
                        "detail": "Not found."
                    }
                }
            ),
            500: openapi.Response(
                description="❌ Internal server error",
                examples={
                    "application/json": {
                        "detail": "Internal server error occurred"
                    }
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update category",
        operation_description="""
        Update an existing category (Admin only).
        
        **Request Body:**
        ```json
        {
            "title": "Updated Category",
            "description": "Updated description",
            "image": "updated_image.jpg",
            "is_active": true
        }
        ```
        
        **Authentication Required:**
        - Admin user only
        - Include JWT token in Authorization header
        - Format: `Bearer <access_token>`
        
        **Response Codes:**
        - **200 OK**: Category updated successfully
        - **400 Bad Request**: Validation errors
        - **401 Unauthorized**: Authentication required
        - **403 Forbidden**: Admin access required
        - **404 Not Found**: Category not found
        - **500 Internal Server Error**: Server error
        """,
        request_body=CategorySerializer,
        responses={
            200: openapi.Response(
                description="✅ Category updated successfully",
                schema=CategorySerializer,
                examples={
                    "application/json": {
                        "id": 1,
                        "title": "Updated Electronics",
                        "description": "Updated electronic devices and gadgets",
                        "image": "http://127.0.0.1:8001/media/categories/updated_electronics.jpg",
                        "is_active": True,
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-15T11:30:00Z"
                    }
                }
            ),
            400: openapi.Response(
                description="❌ Validation errors",
                examples={
                    "application/json": {
                        "title": ["This field is required."],
                        "description": ["This field is required."]
                    }
                }
            ),
            401: openapi.Response(
                description="❌ Authentication required",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
            403: openapi.Response(
                description="❌ Admin access required",
                examples={
                    "application/json": {
                        "detail": "You do not have permission to perform this action."
                    }
                }
            ),
            404: openapi.Response(
                description="❌ Category not found",
                examples={
                    "application/json": {
                        "detail": "Not found."
                    }
                }
            ),
            500: openapi.Response(
                description="❌ Internal server error",
                examples={
                    "application/json": {
                        "detail": "Internal server error occurred"
                    }
                }
            )
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Delete category",
        operation_description="""
        Delete a category (Admin only).
        
        **Authentication Required:**
        - Admin user only
        - Include JWT token in Authorization header
        - Format: `Bearer <access_token>`
        
        **Warning:**
        - This action cannot be undone
        - Related products will be affected
        
        **Response Codes:**
        - **204 No Content**: Category deleted successfully
        - **401 Unauthorized**: Authentication required
        - **403 Forbidden**: Admin access required
        - **404 Not Found**: Category not found
        - **500 Internal Server Error**: Server error
        """,
        responses={
            204: openapi.Response(
                description="✅ Category deleted successfully",
                examples={
                    "application/json": {}
                }
            ),
            401: openapi.Response(
                description="❌ Authentication required",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
            403: openapi.Response(
                description="❌ Admin access required",
                examples={
                    "application/json": {
                        "detail": "You do not have permission to perform this action."
                    }
                }
            ),
            404: openapi.Response(
                description="❌ Category not found",
                examples={
                    "application/json": {
                        "detail": "Not found."
                    }
                }
            ),
            500: openapi.Response(
                description="❌ Internal server error",
                examples={
                    "application/json": {
                        "detail": "Internal server error occurred"
                    }
                }
            )
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)