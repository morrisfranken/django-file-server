# -*- coding: future_fstrings -*-
import os
from os.path import join, basename
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_delete

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<user_id>/<filename>
    return join(str(instance.user.id), filename)

class Uploads(models.Model):
    file            = models.FileField(upload_to=user_directory_path)
    is_private      = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    downloads       = models.IntegerField(default=0)
    size            = models.BigIntegerField(default=0)
    user            = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

@receiver(pre_delete, sender=Uploads)
def delete_Model3D(sender, instance, **kwargs):
    print(f"deleting {instance.file.path}")
    os.remove(instance.file.path)
