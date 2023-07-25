from django.contrib import admin
from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline

# Register your models here.
#Inline class for managing tags in product
class TagInline(GenericTabularInline):
    # Specify the model to be used
    model = TaggedItem
    # Specify the autocomplete fields
    autocomplete_fields = ['tag']

# Register the inline class with the ProductAdmin
class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]

# Unregister the Product class
admin.site.unregister(Product)
# Register the CustomProductAdmin class
admin.site.register(Product, CustomProductAdmin)