from django.contrib import admin
from . import models

# Register Collection model
admin.site.register(models.Collection)
# Register Product model
admin.site.register(models.Product)