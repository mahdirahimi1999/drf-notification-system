from django.conf import settings

from notification_system.tasks import notification_system_send_email


class NotificationHandler:
    TYPE_EMAIL = 1
    EMAIL_NOTIFICATION_QUEUE_NAME = getattr(settings, 'EMAIL_NOTIFICATION_QUEUE_NAME', 'send_email_notification')

    def __init__(self, subject, recipient, email_from, context, content='', notification_type=TYPE_EMAIL,
                 notification_event=None, user_id=None, smtp_config=None, attachments=None):
        """
        :param subject: This field specifies the notification subject
        :type subject: str
        :param recipient: The recipient of the notification is specified in this field
        :type recipient: str
        :param email_from: In this field, you specify the email address of the sender
        :type email_from: str
        :param context: This field specifies extra info for notification
        :type context: dict
        :param content: This field specifies mail template.
        :type content: str
        :param notification_type: This field specifies the notification type
        :type notification_type: int
        :param notification_event: This field specifies the notification_event id
        :type notification_event: int
        :param user_id: This field specifies the user_id
        :type user_id: int
        :param smtp_config: This field specifies the smtp_config
        :type smtp_config: dict
        :param attachments: The attachments of this notification are specified in this field
        :type attachments: list
        """
        self.subject = subject
        self.recipient = recipient
        self.email_from = email_from
        self.context = context
        self.content = content
        self.notification_event = notification_event
        self.user_id = user_id
        self.smtp_config = smtp_config
        self.attachments = attachments
        self.notification_type = notification_type

    def send(self):
        kwargs = {
            'subject': self.subject,
            'recipient': self.recipient,
            'email_from': self.email_from,
            'context': self.context,
            'content': self.content,
            'notification_event': self.notification_event,
            'user_id': self.user_id,
            'smtp_config': self.smtp_config,
            'attachments': self.attachments,
        }
        notification_system_send_email.apply_async(kwargs=kwargs, queue=self.EMAIL_NOTIFICATION_QUEUE_NAME)
