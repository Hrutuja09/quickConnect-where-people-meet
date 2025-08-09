import json
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    return Response({
        'username': request.user.username,
        'email': request.user.email
    })

@api_view(['GET'])
def api_home(request):
    return Response({"message": "Welcome to QuickConnect API"})

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user"""
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=400)

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User registered successfully'})

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Token-based login"""
    username = request.data.get('username')
    password = request.data.get('password')

    # Check if user exists before trying to authenticate
    if not User.objects.filter(username=username).exists():
        return Response({'error': 'User not registered'}, status=404)

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=400)

    # Get or create token
    token, _ = Token.objects.get_or_create(user=user)

    return Response({'message': 'Login successful', 'token': token.key})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    """Token-based logout"""
    request.auth.delete()  # delete token
    return Response({'message': 'Logged out successfully'})

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    username = request.data.get("username")
    new_password = request.data.get("password")

    try:
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        return JsonResponse({"message": "Password updated successfully"}, status=200)
    except User.DoesNotExist:
        return JsonResponse({"error": "Username not found"}, status=404)
