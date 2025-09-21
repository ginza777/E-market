from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    Creates a new user account with email-based authentication.
    """
    password = serializers.CharField(
        write_only=True, 
        validators=[validate_password],
        help_text="Password must be at least 8 characters long and contain letters and numbers."
    )
    password_confirm = serializers.CharField(
        write_only=True,
        help_text="Must match the password field."
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'password', 'password_confirm')
        extra_kwargs = {
            'email': {'help_text': 'Valid email address (will be used for login)'},
            'username': {'help_text': 'Unique username (3-30 characters)'},
            'first_name': {'help_text': 'User\'s first name'},
            'last_name': {'help_text': 'User\'s last name'},
            'phone_number': {'help_text': 'Optional phone number'},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    
    Authenticates user with email and password.
    """
    email = serializers.EmailField(
        help_text="User's email address"
    )
    password = serializers.CharField(
        help_text="User's password"
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password')


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information.
    
    Returns user details for authenticated users.
    """
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'full_name', 'phone_number', 'is_verified', 'created_at')
        read_only_fields = ('id', 'is_verified', 'created_at')
        extra_kwargs = {
            'email': {'help_text': 'User\'s email address'},
            'username': {'help_text': 'User\'s username'},
            'first_name': {'help_text': 'User\'s first name'},
            'last_name': {'help_text': 'User\'s last name'},
            'phone_number': {'help_text': 'User\'s phone number'},
            'is_verified': {'help_text': 'Whether the user\'s email is verified'},
            'created_at': {'help_text': 'Account creation date'},
        }
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
