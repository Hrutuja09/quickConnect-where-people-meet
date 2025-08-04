from django.urls import path
from .views import posts_view,my_posts_view

urlpatterns = [
    path("posts/", posts_view),
    path("my-posts/", my_posts_view),
]
