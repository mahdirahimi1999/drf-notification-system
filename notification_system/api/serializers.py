from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, exceptions

from notification_system.models import (NotificationEvent, EmailTemplate, Attachment, SmtpProvider, NotificationGroup,
                                        OutgoingMessage)


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'file']


class EmailTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTemplate
        fields = ['id', 'title', 'subject', 'content']


class MinimalSmtpProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SmtpProvider
        fields = ['id', 'provider_name']


class MinimalNotificationGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationGroup
        fields = ['id', 'name']


class NotificationEventSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, required=False)
    template_detail = EmailTemplateSerializer(source='template', read_only=True)
    smtp_provider_detail = MinimalSmtpProviderSerializer(source='smtp_provider', read_only=True)
    notification_group_detail = MinimalNotificationGroupSerializer(source='notification_group', read_only=True)

    class Meta:
        model = NotificationEvent
        fields = ['id', 'title', 'smtp_provider', 'smtp_provider_detail', 'template', 'template_detail', 'subject',
                  'content', 'notification_group', 'notification_group_detail', 'attachments']

        extra_kwargs = {
            'template': {'write_only': True},
            'smtp_provider': {'write_only': True},
            'notification_group': {'write_only': True},
        }

    def create(self, validated_data):
        attachments = validated_data.pop('attachments', list())
        instance = super().create(validated_data)

        for attachment in attachments:
            instance.attachments.create(file=attachment.get('file'))

        return instance

    def validate_template(self, value):
        if (not value.is_active) or (not self.context['request'].user == value.owner):
            raise exceptions.ValidationError(detail=_("You do not have permission to access this template."))
        return value

    def validate_notification_group(self, value):
        if (not value.is_active) or (not self.context['request'].user == value.owner):
            raise exceptions.ValidationError(detail=_("You do not have permission to access this notification group."))
        return value

    def validate_smtp_provider(self, value):
        if (not value.is_active) or (not value.users.filter(pk__in=[self.context['request'].user.id]).exists()):
            raise exceptions.ValidationError(detail=_("You do not have permission to access this smtp provider."))
        return value


class MinimalNotificationEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationEvent
        fields = ['id', 'title']


class OutgoingMessageSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    outgoing_message_type_display = serializers.CharField(source="get_outgoing_message_type_display", read_only=True)
    notification_event_detail = MinimalNotificationEventSerializer(source='notification_event', read_only=True)

    class Meta:
        model = OutgoingMessage
        fields = ['id', 'notification_event_detail', 'recipient', 'subject', 'status', 'status_display',
                  'outgoing_message_type', 'outgoing_message_type_display']


class OutgoingMessageNotificationSerializer(serializers.Serializer):
    notificationType = serializers.CharField(label='notification')
    mail = serializers.DictField(write_only=True)
    outgoing_message_id = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs=attrs)
        flag_check_condition = True
        for mail_header in attrs.get('mail', dict()).get('headers'):
            name = mail_header.get('name')
            value = mail_header.get('value')
            if (name == 'outgoing_message_id') and value:
                if value.isdigit():
                    attrs['outgoing_message_id'] = value
                    flag_check_condition = False

        if flag_check_condition:
            raise exceptions.ParseError(_("The payload is not valid."))

        return attrs
