from django.contrib import admin

from notification_system.models import (SmtpProvider, EmailTemplate, Attachment, NotificationGroup, NotificationEvent,
                                        OutgoingMessage)


@admin.register(NotificationGroup)
class NotificationGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'owner', 'is_active', 'created_time', 'updated_time']
    list_filter = ['is_active', 'created_time', 'updated_time']
    search_fields = ['name']
    filter_horizontal = ['members']
    raw_id_fields = ['owner']
    readonly_fields = ['created_time', 'updated_time']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('members').select_related('owner').all()


@admin.register(SmtpProvider)
class SmtpProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'provider_name', 'email_host', 'email_host_user', 'email_port', 'email_use_tls',
                    'email_use_ssl', 'is_active']
    list_filter = ['is_active', 'email_use_tls', 'email_use_ssl', 'created_time', 'updated_time']
    search_fields = ['provider_name']
    filter_horizontal = ['users']
    readonly_fields = ['created_time', 'updated_time']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('users').all()


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'subject', 'is_active', 'created_time', 'updated_time']
    list_filter = ['is_active', 'created_time', 'updated_time']
    readonly_fields = ['created_time', 'updated_time']
    raw_id_fields = ['owner']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('owner').all()


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'notification_event', 'created_time', 'updated_time']
    list_filter = ['created_time', 'updated_time']
    raw_id_fields = ['notification_event']
    readonly_fields = ['created_time', 'updated_time']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('notification_event').all()


class AttachmentInline(admin.TabularInline):
    model = Attachment


@admin.register(NotificationEvent)
class NotificationEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'owner', 'smtp_provider', 'template', 'is_active', 'created_time', 'updated_time']
    list_filter = ['is_active', 'created_time', 'updated_time']
    raw_id_fields = ['owner', 'smtp_provider', 'notification_group', 'template']
    readonly_fields = ['created_time', 'updated_time']
    inlines = [AttachmentInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('attachments').select_related('smtp_provider', 'owner',
                                                                       'notification_group', 'template').all()


@admin.register(OutgoingMessage)
class OutgoingMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'notification_event', 'user', 'recipient', 'subject', 'status', 'outgoing_message_type',
                    'created_time', 'updated_time']
    list_filter = ['status', 'outgoing_message_type', 'notification_event', 'created_time', 'updated_time']
    raw_id_fields = ['user', 'notification_event']
    readonly_fields = ['created_time', 'updated_time']
    search_fields = ['recipient']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user', 'notification_event').all()
