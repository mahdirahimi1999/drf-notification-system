# DRF Notification System

**An app that sends notifications to internal users.**

# Requirements

- Django (2.2 <= 3.2 )
- Django REST framework
- django_filters
- Celery

# Installation

-   `pip install drf-notification-system`

# Post-Install Setup
**Django Settings**

```python
INSTALLED_APPS = [
    ...
    'notification_system',
]

```

Include the notification system urls in your project urls.py like this
```python
path('notification-system/', include('notification_system.urls')),
```

- Run `python manage.py migrate` to create the notification system models.


- If you want to change send email notification default queue name, set `EMAIL_NOTIFICATION_QUEUE_NAME` constance on the `settings.py` file. the default value is 'send_email_notification'


- If you want to change send update outgoing message status default queue name, set `UPDATE_OUTGOING_MESSAGE_STATUS_QUEUE_NAME` constance on the `settings.py` file. the default value is 'update_outgoing_message_status'


- If you want to change send email notification rate limit, set `NOTIFICATION_SYSTEM_SEND_EMAIL_RATE_LIMIT` constance on the `settings.py` file. the default value is '700/m'


- If you want to change user fields to pass template as context data, set `NOTIFICATION_SYSTEM_DEFAULT_USER_FIELD` constance on the `settings.py` file. the default value is ['id', 'username', 'first_name', 'last_name', 'email']


- Run Celery worker with the following command

    `celery -A 'project_name' worker --loglevel DEBUG -Q 'queue_name' --concurrency=1`
    
    `celery -A 'project_name' worker --loglevel DEBUG -Q send_email_notification --concurrency=1`
    
    `celery -A 'project_name' worker --loglevel DEBUG -Q update_outgoing_message_status --concurrency=1`