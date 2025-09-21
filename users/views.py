from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint.
    
    Creates a new user account with email verification.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="""
        Create a new user account with email and password.
        
        **Request Body:**
        ```json
        {
            "email": "user@example.com",
            "username": "johndoe",
            "first_name": "John",
            "last_name": "Doe",
            "password": "securepassword123",
            "password_confirm": "securepassword123",
            "phone_number": "+1234567890"
        }
        ```
        
        **Requirements:**
        - Email must be unique and valid
        - Username must be unique (3-30 characters)
        - Password must be at least 8 characters
        - First name and last name are required
        - Password and password_confirm must match
        
        **Response Codes:**
        - **201 Created**: User created successfully
        - **400 Bad Request**: Validation errors
        - **500 Internal Server Error**: Server error
        """,
        request_body=UserRegistrationSerializer,
        responses={
            201: openapi.Response(
                description="✅ User created successfully",
                schema=UserSerializer,
                examples={
                    "application/json": {
                        "id": 1,
                        "email": "user@example.com",
                        "username": "johndoe",
                        "first_name": "John",
                        "last_name": "Doe",
                        "full_name": "John Doe",
                        "phone_number": "+1234567890",
                        "is_verified": False,
                        "is_active": True,
                        "is_staff": False,
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-15T10:30:00Z"
                    }
                }
            ),
            400: openapi.Response(
                description="❌ Validation errors",
                examples={
                    "application/json": {
                        "email": ["A user with this email already exists."],
                        "username": ["A user with this username already exists."],
                        "password": ["This password is too short. It must contain at least 8 characters."],
                        "password_confirm": ["Passwords do not match."],
                        "first_name": ["This field is required."],
                        "last_name": ["This field is required."]
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


@api_view(['POST'])
@permission_classes([AllowAny])
@swagger_auto_schema(
    operation_summary="User login",
    operation_description="""
    Authenticate user and return JWT tokens.
    
    **Request Body:**
    ```json
    {
        "email": "user@example.com",
        "password": "securepassword123"
    }
    ```
    
    **Process:**
    1. Validate email and password
    2. Check if user exists and is active
    3. Generate JWT access and refresh tokens
    4. Return user profile and tokens
    
    **Security:**
    - Tokens expire after configured time
    - Refresh token can be used to get new access token
    
    **Response Codes:**
    - **200 OK**: Login successful
    - **400 Bad Request**: Invalid credentials
    - **401 Unauthorized**: Authentication failed
    - **500 Internal Server Error**: Server error
    """,
    request_body=UserLoginSerializer,
    responses={
        200: openapi.Response(
            description="✅ Login successful",
            examples={
                "application/json": {
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "username": "johndoe",
                        "first_name": "John",
                        "last_name": "Doe",
                        "full_name": "John Doe",
                        "phone_number": "+1234567890",
                        "is_verified": False,
                        "is_active": True,
                        "is_staff": False,
                        "created_at": "2024-01-15T10:30:00Z",
                        "updated_at": "2024-01-15T10:30:00Z"
                    }
                }
            }
        ),
        400: openapi.Response(
            description="❌ Invalid credentials",
            examples={
                "application/json": {
                    "detail": "Invalid email or password"
                }
            }
        ),
        401: openapi.Response(
            description="❌ Authentication failed",
            examples={
                "application/json": {
                    "detail": "Authentication credentials were not provided."
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
def login_view(request):
    """
    User login endpoint.
    
    Authenticates user and returns JWT tokens.
    """
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@swagger_auto_schema(
    operation_summary="Refresh JWT token",
    operation_description="""
    Refresh JWT access token using refresh token.
    
    **Request Body:**
    ```json
    {
        "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```
    
    **Process:**
    1. Validate refresh token
    2. Generate new access token
    3. Return new access token
    
    **Response Codes:**
    - **200 OK**: Token refreshed successfully
    - **400 Bad Request**: Invalid refresh token
    - **401 Unauthorized**: Token expired or invalid
    - **500 Internal Server Error**: Server error
    """,
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='JWT refresh token'
            )
        },
        required=['refresh']
    ),
    responses={
        200: openapi.Response(
            description="✅ Token refreshed successfully",
            examples={
                "application/json": {
                    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                }
            }
        ),
        400: openapi.Response(
            description="❌ Invalid refresh token",
            examples={
                "application/json": {
                    "detail": "Token is invalid or expired"
                }
            }
        ),
        401: openapi.Response(
            description="❌ Token expired",
            examples={
                "application/json": {
                    "detail": "Token has expired"
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
def refresh_token_view(request):
    """
    Refresh JWT token endpoint.
    
    Generates new access token using refresh token.
    """
    try:
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'detail': 'Refresh token is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        
        return Response({
            'access': access_token
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'detail': 'Token is invalid or expired'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@swagger_auto_schema(
    operation_summary="Get user profile",
    operation_description="""
    Get current user's profile information.
    
    **Authentication Required:**
    - Include JWT token in Authorization header
    - Format: `Bearer <access_token>`
    
    **Response Codes:**
    - **200 OK**: Profile retrieved successfully
    - **401 Unauthorized**: Authentication required
    - **403 Forbidden**: Access denied
    - **500 Internal Server Error**: Server error
    """,
    responses={
        200: openapi.Response(
            description="✅ Profile retrieved successfully",
            schema=UserSerializer,
            examples={
                "application/json": {
                    "id": 1,
                    "email": "user@example.com",
                    "username": "johndoe",
                    "first_name": "John",
                    "last_name": "Doe",
                    "full_name": "John Doe",
                    "phone_number": "+1234567890",
                    "is_verified": False,
                    "is_active": True,
                    "is_staff": False,
                    "created_at": "2024-01-15T10:30:00Z",
                    "updated_at": "2024-01-15T10:30:00Z"
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
            description="❌ Access denied",
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
def profile_view(request):
    """
    User profile endpoint.
    
    Returns current user's profile information.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)