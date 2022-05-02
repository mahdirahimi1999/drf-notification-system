from django.urls import path
from rest_framework import routers

from notification_system.api.views import (NotificationEventViewSet, EmailTemplateViewSet, OutgoingMessageViewSet,
                                           OutgoingMessageNotificationAPIView, NotificationGroupViewSet,
                                           SmtpProviderViewSet)

app_name = "notification_events"

router = routers.SimpleRouter()
router.register("notification-events", NotificationEventViewSet, basename="notification_events")
router.register("email-templates", EmailTemplateViewSet, basename="email_templates")
router.register("outgoing-messages", OutgoingMessageViewSet, basename="outgoing_messages")
router.register("notification-groups", NotificationGroupViewSet, basename="notification_groups")
router.register("smtp-providers", SmtpProviderViewSet, basename="smtp_providers")

urlpatterns = router.urls

urlpatterns += [
    path("outgoing-message-webhook/", OutgoingMessageNotificationAPIView.as_view(), name="outgoing_message_webhook"),
]
