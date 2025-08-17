from django.urls import path
from .views import mark_notification_read,NotificationList

urlpatterns = [
    path("notification-list/",NotificationList.as_view()),
    path("notification/<int:pk>/read/", mark_notification_read),
]
