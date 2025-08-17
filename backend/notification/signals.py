from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Comment, Like, Notification

@receiver(post_save, sender=Comment)
def comment_notification(sender, instance, created, **kwargs):
    if created:
        post_author = instance.post.author
        commenter = instance.user
        if commenter != post_author:
            message = f"{commenter.username} commented on your post."
            Notification.objects.create(user=post_author, message=message)

@receiver(post_save, sender=Like)
def like_notification(sender, instance, created, **kwargs):
    if created:
        post_author = instance.post.author
        liker = instance.user
        if liker != post_author:
            message = f"{liker.username} liked your post."
            Notification.objects.create(user=post_author, message=message)
