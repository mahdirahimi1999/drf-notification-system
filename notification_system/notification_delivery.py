from notification_system.common.notification_handler import NotificationHandler
from notification_system.models import NotificationEvent
from notification_system.utils import get_user_common_data


def broadcast_event_messages_to_recipients(event_message_id):
    notification_event = NotificationEvent.objects.prefetch_related('notification_group__members', 'attachments') \
        .select_related('smtp_provider', 'owner', 'notification_group', 'template').get(id=event_message_id)

    subject = notification_event.get_subject()
    html_content = notification_event.get_content()
    users = notification_event.notification_group.members.filter(is_active=True)
    email_from = notification_event.smtp_provider.email_from
    smtp_config = notification_event.smtp_provider.get_smtp_config()
    attachments = [attachment.file.path for attachment in notification_event.attachments.all()]

    for user in users:
        context = get_user_common_data(user=user)
        notification_handler = NotificationHandler(subject=subject, recipient=user.email, email_from=email_from,
                                                   context=context, content=html_content, user_id=user.id,
                                                   smtp_config=smtp_config, attachments=attachments,
                                                   notification_event=notification_event.id)
        notification_handler.send()

    return True
