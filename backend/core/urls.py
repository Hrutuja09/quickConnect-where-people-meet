
from django.urls import path
from .views import *;

urlpatterns = [
    path("", api_home),
    path('me/', current_user),
    path('register/', register),
    path('login/', login_view),
    path('logout/', logout),
    path('reset-password/',reset_password),
]
