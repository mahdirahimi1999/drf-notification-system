from django.db import models


class ActiveManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
