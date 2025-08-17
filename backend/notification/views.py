from rest_framework import generics, permissions
from core.models import Notification
from .serializers import NotificationSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

class NotificationList(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')
    

@permission_classes([permissions.IsAuthenticated])
@api_view(['POST'])
def mark_notification_read(request,pk):
    try:
        notif = Notification.objects.get(pk=pk,user=request.user)
    except Notification.DoesNotExist:
        return Response({'error':'Not Found'},status=404)
    notif.is_read=True
    notif.save()
    return Response({"sucess": "Marked as read"})






