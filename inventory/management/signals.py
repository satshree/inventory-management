from django.dispatch import receiver
from management.models import Company
from django.db import models
import os

@receiver(models.signals.post_delete, sender=Company)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.logo:
        if os.path.isfile(instance.logo.path):
            os.remove(instance.logo.path)

@receiver(models.signals.pre_save, sender=Company)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = Company.objects.get(pk=instance.pk).logo
    except Company.DoesNotExist:
        return False

    new_file = instance.logo
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)