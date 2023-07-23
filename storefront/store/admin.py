from django.contrib import admin
from . import models

# Class ProductAdmin is used to customize the admin panel for Product model
@admin.register(models.Product) #Decorator for registering the Product admin with Product model
class ProductAdmin(admin.ModelAdmin):
    # Specify the fields to be displayed in the admin panel
    list_display = ['title', 'unit_price', 'inventory_status']
    # Specify the fields that can be edited
    list_editable = ['unit_price']
    # Limit the number of objects displayed in the admin panel
    list_per_page = 10
    # Specify the fields to be used for filtering
    # list_filter = ('collection', 'last_update')
    # # Specify the fields to be used for searching
    # search_fields = ('title', 'description')
    # # Specify the fields to be used for ordering
    # ordering = ['title']

    # Define a method for computing inventory status based on inventory size
    @admin.display(ordering='inventory') # Decorator for sorting the inventory column
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

# Register Customer model
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    # Specify the fields to be displayed in the admin panel
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10

# Register Collection model
admin.site.register(models.Collection)
# Register Product model
# admin.site.register(models.Product, ProductAdmin) # Add ProductAdmin for passing in the customized admin panel