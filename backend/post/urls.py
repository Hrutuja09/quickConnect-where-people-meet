from django.urls import path
from .views import posts_view,my_posts_view,random_posts_view,add_comment, like_post

urlpatterns = [
    path("posts/", posts_view),
    path("my-posts/", my_posts_view),
    path("random-posts/",random_posts_view),
    path("posts/<int:pk>/comment/", add_comment),
    path("posts/<int:post_id>/like/", like_post),
]
