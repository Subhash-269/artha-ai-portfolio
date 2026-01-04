from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'email', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name (optional)'),
            'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name (optional)'),
        },
    ),
    responses={
        201: openapi.Response(
            description='User created successfully',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication token'),
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                }
            )
        ),
        400: 'Bad Request - Validation errors'
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    Register a new user account
    """
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')

    # Validate required fields
    if not username or not email or not password:
        return Response(
            {'error': 'Username, email, and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if email already exists
    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already registered'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create user
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
        },
    ),
    responses={
        200: openapi.Response(
            description='Login successful',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING, description='Authentication token'),
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                }
            )
        ),
        401: 'Invalid credentials'
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    """
    Login with username and password
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Create or get token
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@swagger_auto_schema(
    method='post',
    responses={
        200: 'Logout successful',
        401: 'Not authenticated'
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    """
    Logout the current user (deletes auth token)
    """
    try:
        # Delete the user's token to logout
        request.user.auth_token.delete()
        return Response(
            {'message': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@swagger_auto_schema(
    method='get',
    responses={
        200: openapi.Response(
            description='User info',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                    'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email'),
                    'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First name'),
                    'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last name'),
                }
            )
        ),
        401: 'Not authenticated'
    }
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """
    Get current user information
    """
    user = request.user
    return Response({
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
    }, status=status.HTTP_200_OK)
