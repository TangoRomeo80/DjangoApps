from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class LikedItem(models.Model):
    # What user liked what object
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Type of object
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # Primary key of object
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()