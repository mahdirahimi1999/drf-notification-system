import os

from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _


def validate_file_extension(value):
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xlsx', '.xls', '.mp3']
    file_extension = os.path.splitext(value.name)[-1]
    if not file_extension.lower() in valid_extensions:
        raise ValidationError(_("Unsupported file extension. valid extensions: {}".format(valid_extensions)))


def validate_file_size(value):
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(_("File too large. Size should not exceed {}.".format(filesizeformat(limit))))
