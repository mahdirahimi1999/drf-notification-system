from django.conf import settings


def get_user_common_data(user):
    default_user_field = getattr(settings, 'NOTIFICATION_SYSTEM_DEFAULT_USER_FIELD',
                                 ['id', 'username', 'first_name', 'last_name', 'email'])
    return {key: getattr(user, key, '') for key in default_user_field}
