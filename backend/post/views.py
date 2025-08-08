
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from core.models import Post,Comment, Like

from .serializers import PostSerializer,CommentSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def posts_view(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_posts_view(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def random_posts_view(request):
    posts = Post.objects.exclude(author=request.user).order_by('?')[:10]
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)

    text = request.data.get("text")
    if not text:
        return Response({"error": "Comment text is required"}, status=400)

    comment = Comment.objects.create(post=post, user=request.user, text=text)
    serializer = CommentSerializer(comment)
    return Response(serializer.data, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    """To handle the like for a post"""
    user = request.user

    """Check if the post exists"""
    try:
        post = Post.objects.get(id=post_id)
    except:
        return Response({"error":"Post not found!"}, status=404)
    
    """Check if the post is already liked"""
    if Like.objects.filter(user=user,post=post).exists():
        return Response({"message":"Post already liked","likes_count":post.likes.count()} ,status=200)
    
    Like.objects.create(user=user,post=post)
    return Response({"message":"Post liked successfully", "likes_count":post.likes.count()},status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_post(request, post_id):
    """To handle the unlike for a post"""
    user = request.user

    """Check if the post exists"""
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({"error":"Post not found!"}, status=404)
    
    """Check if the post is already liked"""
    try:
        like=Like.objects.get(user=user,post=post)
        like.delete()
        return Response({"message":"Post is unliked","likes_count":post.likes.count()} ,status=200)
    except Post.DoesNotExist:
        return Response({"message":"Post is not liked ", "likes_count":post.likes.count()},status=200)
    




