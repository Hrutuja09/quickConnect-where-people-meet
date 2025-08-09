
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
    user = request.user
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    like_obj = Like.objects.filter(post=post, user=user)
    if like_obj.exists():
        # User already liked the post; unlike it
        like_obj.delete()
        liked = False
    else:
        # Like the post
        Like.objects.create(post=post, user=user)
        liked = True

    # Return updated like count and status
    likes_count = post.likes.count()  # count of all likes for this post
    return Response({
        'liked': liked,
        'likes_count': likes_count,
        'message': 'Liked' if liked else 'Unliked'
    })



