from typing import cast
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

def user_upload_dir(instance, filename):
    return 'users_img/user_{0}/{1}'.format(instance.user.id, filename)

class Image(models.Model):
    title = models.CharField(max_length=100)
    width = models.IntegerField()
    height = models.IntegerField()
    file = models.ImageField(upload_to=user_upload_dir)
    created_at = models.DateTimeField(auto_created=True, auto_now=True)
    user = models.ForeignKey(User, on_delete=CASCADE, null=True)

class Descriptor(models.Model):
    rows = models.IntegerField()
    cols = models.IntegerField()
    content = models.CharField(max_length=10000)
    image = models.OneToOneField(Image, on_delete=CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_created=True, auto_now=True)