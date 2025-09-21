from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Product
from .serializers import ProductSerializer
from .documents import ProductDocument, ProductDocumentSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    Product management endpoint.
    
    Provides CRUD operations for products with advanced filtering, search, and Elasticsearch integration.
    """
    queryset = Product.objects.filter(is_active=True).select_related('category')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'price', 'created_at']
    ordering = ['-created_at']
    filterset_fields = ['category', 'is_active']
    
    @swagger_auto_schema(
        operation_summary="List all products",
        operation_description="""
        Retrieve a paginated list of active products.
        
        **Features:**
        - Pagination support (default: 20 items per page)
        - Search by title and description
        - Order by title, price, or creation date
        - Filter by category and active status
        - Includes category information
        
        **Query Parameters:**
        - `search`: Search in title and description
        - `ordering`: Sort by field (prefix with - for descending)
        - `category`: Filter by category ID
        - `is_active`: Filter by active status
        - `page`: Page number for pagination
        """,
        responses={
            200: openapi.Response(
                description="Products retrieved successfully",
                examples={
                    "application/json": {
                        "count": 100,
                        "next": "http://api.example.com/products/?page=2",
                        "previous": None,
                        "results": [
                            {
                                "id": 1,
                                "title": "iPhone 15 Pro",
                                "description": "Latest iPhone with advanced features",
                                "price": "999.99",
                                "image": "http://api.example.com/media/products/iphone15.jpg",
                                "category": {
                                    "id": 1,
                                    "title": "Electronics",
                                    "description": "Electronic devices"
                                },
                                "is_active": True,
                                "stock_quantity": 25,
                                "created_at": "2023-01-01T00:00:00Z",
                                "updated_at": "2023-01-01T00:00:00Z"
                            }
                        ]
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request - Invalid query parameters",
                examples={
                    "application/json": {
                        "ordering": ["Invalid ordering field"],
                        "category": ["Invalid category ID"]
                    }
                }
            ),
            500: openapi.Response(
                description="Internal Server Error",
                examples={
                    "application/json": {
                        "detail": "Internal server error occurred"
                    }
                }
            )
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Create a new product",
        operation_description="""
        Create a new product.
        
        **Authentication Required:**
        - Must be authenticated user
        - Include JWT token in Authorization header
        
        **Required Fields:**
        - title: Product name
        - description: Product description
        - price: Product price (decimal)
        - category: Category ID
        - stock_quantity: Available stock
        
        **Optional Fields:**
        - image: Product image file
        """,
        request_body=ProductSerializer,
        responses={
            201: openapi.Response(
                description="Product created successfully",
                schema=ProductSerializer,
                examples={
                    "application/json": {
                        "id": 1,
                        "title": "iPhone 15 Pro",
                        "description": "Latest iPhone with advanced features",
                        "price": "999.99",
                        "image": "http://api.example.com/media/products/iphone15.jpg",
                        "category": {
                            "id": 1,
                            "title": "Electronics",
                            "description": "Electronic devices"
                        },
                        "is_active": True,
                        "stock_quantity": 25,
                        "created_at": "2023-01-01T00:00:00Z",
                        "updated_at": "2023-01-01T00:00:00Z"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request - Validation errors",
                examples={
                    "application/json": {
                        "title": ["This field is required."],
                        "price": ["A valid number is required."],
                        "category": ["Invalid pk \"999\" - object does not exist."],
                        "stock_quantity": ["Ensure this value is greater than or equal to 0."]
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized - Authentication required",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
            403: openapi.Response(
                description="Forbidden - Insufficient permissions",
                examples={
                    "application/json": {
                        "detail": "You do not have permission to perform this action."
                    }
                }
            )
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Get product details",
        operation_description="""
        Retrieve detailed information about a specific product.
        
        **Returns:**
        - Complete product information
        - Category details
        - Image URL if available
        - Stock information
        """,
        responses={
            200: openapi.Response(
                description="Product details retrieved successfully",
                schema=ProductSerializer,
                examples={
                    "application/json": {
                        "id": 1,
                        "title": "iPhone 15 Pro",
                        "description": "Latest iPhone with advanced features",
                        "price": "999.99",
                        "image": "http://api.example.com/media/products/iphone15.jpg",
                        "category": {
                            "id": 1,
                            "title": "Electronics",
                            "description": "Electronic devices"
                        },
                        "is_active": True,
                        "stock_quantity": 25,
                        "created_at": "2023-01-01T00:00:00Z",
                        "updated_at": "2023-01-01T00:00:00Z"
                    }
                }
            ),
            404: openapi.Response(
                description="Not Found - Product does not exist",
                examples={
                    "application/json": {
                        "detail": "Not found."
                    }
                }
            ),
            500: openapi.Response(
                description="Internal Server Error",
                examples={
                    "application/json": {
                        "detail": "Internal server error occurred"
                    }
                }
            )
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Update product",
        operation_description="""
        Update an existing product.
        
        **Authentication Required:**
        - Must be authenticated user
        - Include JWT token in Authorization header
        
        **Fields:**
        - All fields are optional for partial updates
        - Price updates affect stock calculations
        - Image can be updated by uploading new file
        """,
        request_body=ProductSerializer,
        responses={
            200: openapi.Response(
                description="Product updated successfully",
                schema=ProductSerializer,
                examples={
                    "application/json": {
                        "id": 1,
                        "title": "iPhone 15 Pro Max",
                        "description": "Updated description",
                        "price": "1099.99",
                        "image": "http://api.example.com/media/products/iphone15max.jpg",
                        "category": {
                            "id": 1,
                            "title": "Electronics",
                            "description": "Electronic devices"
                        },
                        "is_active": True,
                        "stock_quantity": 30,
                        "created_at": "2023-01-01T00:00:00Z",
                        "updated_at": "2023-01-02T00:00:00Z"
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request - Validation errors",
                examples={
                    "application/json": {
                        "title": ["This field is required."],
                        "price": ["A valid number is required."],
                        "stock_quantity": ["Ensure this value is greater than or equal to 0."]
                    }
                }
            ),
            401: openapi.Response(
                description="Unauthorized - Authentication required",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
            403: openapi.Response(
                description="Forbidden - Insufficient permissions",
                examples={
                    "application/json": {
                        "detail": "You do not have permission to perform this action."
                    }
                }
            ),
            404: openapi.Response(
                description="Not Found - Product does not exist",
                examples={
                    "application/json": {
                        "detail": "Not found."
                    }
                }
            )
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_summary="Delete product",
        operation_description="""
        Delete a product (soft delete - sets is_active=False).
        
        **Authentication Required:**
        - Must be authenticated user
        - Include JWT token in Authorization header
        
        **Note:**
        - This is a soft delete operation
        - Product will be hidden but not permanently removed
        - Elasticsearch index will be updated
        """,
        responses={
            204: openapi.Response(
                description="Product deleted successfully - No content returned"
            ),
            401: openapi.Response(
                description="Unauthorized - Authentication required",
                examples={
                    "application/json": {
                        "detail": "Authentication credentials were not provided."
                    }
                }
            ),
            403: openapi.Response(
                description="Forbidden - Insufficient permissions",
                examples={
                    "application/json": {
                        "detail": "You do not have permission to perform this action."
                    }
                }
            ),
            404: openapi.Response(
                description="Not Found - Product does not exist",
                examples={
                    "application/json": {
                        "detail": "Not found."
                    }
                }
            )
        }
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['get'])
    @swagger_auto_schema(
        operation_summary="Search products with Elasticsearch",
        operation_description="""
        Advanced product search using Elasticsearch.
        
        **Features:**
        - Full-text search across product titles and descriptions
        - Advanced filtering by category, price range, and stock
        - Sorting by relevance, price, or date
        - Fast search performance
        
        **Query Parameters:**
        - `search`: Search query (searches in title and description)
        - `category`: Filter by category ID
        - `min_price`: Minimum price filter
        - `max_price`: Maximum price filter
        - `in_stock`: Filter products with stock > 0
        - `ordering`: Sort by field
        """,
        responses={
            200: openapi.Response(
                description="Search results retrieved successfully",
                examples={
                    "application/json": {
                        "count": 15,
                        "next": "http://api.example.com/products/search/?page=2&search=iPhone",
                        "previous": None,
                        "results": [
                            {
                                "id": 1,
                                "title": "iPhone 15 Pro",
                                "description": "Latest iPhone with advanced features",
                                "price": "999.99",
                                "image": "http://api.example.com/media/products/iphone15.jpg",
                                "category": {
                                    "id": 1,
                                    "title": "Electronics"
                                },
                                "is_active": True,
                                "stock_quantity": 25,
                                "created_at": "2023-01-01T00:00:00Z",
                                "updated_at": "2023-01-01T00:00:00Z"
                            }
                        ]
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request - Invalid search parameters",
                examples={
                    "application/json": {
                        "min_price": ["A valid number is required."],
                        "max_price": ["A valid number is required."]
                    }
                }
            ),
            500: openapi.Response(
                description="Internal Server Error - Elasticsearch unavailable",
                examples={
                    "application/json": {
                        "detail": "Search service temporarily unavailable"
                    }
                }
            )
        }
    )
    def search(self, request):
        """Advanced search using Elasticsearch"""
        try:
            # Get search parameters
            search_query = request.query_params.get('search', '')
            category_id = request.query_params.get('category')
            min_price = request.query_params.get('min_price')
            max_price = request.query_params.get('max_price')
            in_stock = request.query_params.get('in_stock', 'false').lower() == 'true'
            
            # Build Elasticsearch query
            search = ProductDocument.search()
            
            if search_query:
                search = search.query('multi_match', query=search_query, fields=['title', 'description'])
            
            if category_id:
                search = search.filter('term', category__id=category_id)
            
            if min_price or max_price:
                price_range = {}
                if min_price:
                    price_range['gte'] = float(min_price)
                if max_price:
                    price_range['lte'] = float(max_price)
                search = search.filter('range', price=price_range)
            
            if in_stock:
                search = search.filter('range', stock_quantity={'gt': 0})
            
            # Execute search
            response = search.execute()
            
            # Convert to regular serializer format
            products = []
            for hit in response:
                product_data = hit.to_dict()
                product_data['category'] = {
                    'id': product_data['category']['id'],
                    'title': product_data['category']['title']
                }
                products.append(product_data)
            
            # Apply pagination
            page = self.paginate_queryset(products)
            if page is not None:
                serializer = ProductSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'detail': 'Search service temporarily unavailable'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    @swagger_auto_schema(
        operation_summary="Get low stock products",
        operation_description="""
        Retrieve products with low stock levels.
        
        **Use Cases:**
        - Inventory management
        - Restock alerts
        - Stock monitoring
        
        **Query Parameters:**
        - `threshold`: Stock threshold (default: 10)
        - `category`: Filter by category ID
        """,
        responses={
            200: openapi.Response(
                description="Low stock products retrieved successfully",
                examples={
                    "application/json": {
                        "count": 5,
                        "results": [
                            {
                                "id": 1,
                                "title": "iPhone 15 Pro",
                                "description": "Latest iPhone",
                                "price": "999.99",
                                "stock_quantity": 3,
                                "category": {
                                    "id": 1,
                                    "title": "Electronics"
                                },
                                "is_active": True,
                                "created_at": "2023-01-01T00:00:00Z",
                                "updated_at": "2023-01-01T00:00:00Z"
                            }
                        ]
                    }
                }
            ),
            400: openapi.Response(
                description="Bad Request - Invalid threshold",
                examples={
                    "application/json": {
                        "threshold": ["A valid integer is required."]
                    }
                }
            )
        }
    )
    def low_stock(self, request):
        """Get products with low stock"""
        threshold = int(request.query_params.get('threshold', 10))
        category_id = request.query_params.get('category')
        
        queryset = self.get_queryset().filter(stock_quantity__lte=threshold)
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductDocumentViewSet(DocumentViewSet):
    """
    Elasticsearch document viewset for advanced product search.
    
    Provides direct access to Elasticsearch for complex queries.
    """
    document = ProductDocument
    serializer_class = ProductDocumentSerializer
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        SearchFilterBackend,
    ]
    search_fields = (
        'title',
        'description',
    )
    filter_fields = {
        'category.id': 'category.id',
        'price': 'price',
        'stock_quantity': 'stock_quantity',
        'is_active': 'is_active',
    }
    ordering_fields = {
        'created_at': 'created_at',
        'price': 'price',
        'title': 'title',
    }
    ordering = ('-created_at',)