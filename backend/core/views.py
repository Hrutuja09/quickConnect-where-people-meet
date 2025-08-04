import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.middleware.csrf import get_token
from django.http import JsonResponse

@api_view(['GET'])
def get_csrf_token(request):
    return Response({'csrfToken': get_token(request)})

@api_view(['GET'])
def api_home(request):
    return Response({"message": "Welcome to QuickConnect API"})

@api_view(['POST'])
def register(request):
    """Register the user"""
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=400)

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User registered successfully'})

@api_view(['POST'])
def login_view(request):
    """Login for the user if the user already exists"""
    
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    print("Incoming login request data:", request.data)

        # Check if user exists
    if not User.objects.filter(username=username).exists():
        return Response({'error': 'User not registered'}, status=404)

    
    if user is not None:
        login(request, user)
        return Response({'message': 'Login successful'})
    else:
        return Response({'error': 'Invalid credentials'}, status=400)



@api_view(['POST'])
def logout_view(request):
    """Logout functionality for the user to logout"""
    logout(request)
    return Response({'message': 'Logged out successfully'})

def reset_password(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        new_password = data.get("password")

        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return JsonResponse({"message": "Password updated successfully"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "Username not found"}, status=404)


