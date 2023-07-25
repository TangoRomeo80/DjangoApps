from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models
from tags.models import TaggedItem

# class for filtering inventory
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    # Method for filtering the queryset
    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]

    # Method for getting the queryset
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)


# Class ProductAdmin is used to customize the admin panel for Product model
@admin.register(models.Product) #Decorator for registering the Product admin with Product model
class ProductAdmin(admin.ModelAdmin):
    # Customize the creation form
    # exclude = ('created_at', 'updated_at')
    # fields = (('title', 'collection'), 'description', 'slug', ('inventory', 'unit_price'), 'last_update')
    # readonly_fields = ('last_update', 'slug')
    # Prepopulated fields for forms
    prepopulated_fields = {
        'slug': ['title']
    }
    # Autocomplete fields for forms
    autocomplete_fields = ['collection']
    # Actions to be displayed in the admin panel
    actions = ['clear_inventory']
    # Specify the fields to be displayed in the admin panel
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    # Specify the fields that can be edited
    list_editable = ['unit_price']
    # Limit the number of objects displayed in the admin panel
    list_per_page = 10
    # Specify the fields to be used for filtering
    list_filter = ['collection', 'last_update', InventoryFilter]
    # # Specify the fields to be used for searching
    search_fields = ('title', 'description')
    # # Specify the fields to be used for ordering
    # ordering = ['title']
    # speciify fields to be eager loaded
    list_select_related = ['collection']

    # Define a method for computing inventory status based on inventory size
    @admin.display(ordering='inventory') # Decorator for sorting the inventory column
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    # Define a method for getting related field collection title
    def collection_title(self, product):
        return product.collection.title

    # Custom action to clear the inventory
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(request, f'{updated_count} products were successfully updated.', messages.SUCCESS)
        

# Register Customer model
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    # Specify the fields to be displayed in the admin panel
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    # Define a method for getting related field orders count
    @admin.display(ordering='orders_count') # Decorator for sorting the orders_count column
    def orders_count(self, customer):
        url =reverse('admin:store_order_changelist') + '?' + urlencode({
            'customer__id': str(customer.id)
        })
        #Link to the order list page for the customer
        return format_html('<a href="{}">{}</>', url, customer.orders_count)

    #Override the queryset method to get the orders count
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count= Count('order')
        )

# Class to enable inline editing of OrderItem model
class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 0

# Register Order model
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    autocomplete_fields = ['customer']
    # Inline editing of OrderItem model
    inlines = [OrderItemInline]


# Register Collection model
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title__istartswith']

    # Define a method for getting related field products count
    @admin.display(ordering='products_count') # Decorator for sorting the products_count column
    def products_count(self, collection):
        url =reverse('admin:store_product_changelist') + '?' + urlencode({
            'collection__id': str(collection.id)
        })
        #Link to the product list page for the collection
        return format_html('<a href="{}">{}</>', url, collection.products_count)

    #Override the queryset method to get the products count
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count= Count('product')
        )


# Register Product model
# admin.site.register(models.Product, ProductAdmin) # Add ProductAdmin for passing in the customized admin panel