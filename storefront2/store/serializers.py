from rest_framework import serializers
from .models import Product, Collection
from decimal import Decimal


#Serializer is a class that converts model to JSON

# CollectionSerializer is a class that converts Collection model to JSON
# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)

# This is the implementation with ModelSerializer
class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']

# ProductSerializer is a class that converts Product model to JSON
# class ProductSerializer(serializers.Serializer): # This is the implementation with base serializer
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)
#     # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
#     price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    
#     # Custom field that is not in the model but will be created in the JSON
#     price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
#     #Relational fields
#     # pk related field
#     # collection = serializers.PrimaryKeyRelatedField(
#     #     queryset=Collection.objects.all()
#     # )
    
#     # String related field
#     # collection = serializers.StringRelatedField()
    
#     # Including a nested object in the JSON as related field
#     # collection = CollectionSerializer()

#     # Including a hyperlinked object in the JSON as related field
#     collection = serializers.HyperlinkedRelatedField(
#         queryset=Collection.objects.all(),
#         view_name='collection-detail'
#     )

#     def calculate_tax(self, product: Product):
#         return product.unit_price * Decimal(1.1)

# This is the implementation with ModelSerializer
class ProductSerializer(serializers.ModelSerializer):
    # create meta class which will define the fields
    class Meta:
        model = Product
        fields = ['id', 'title','unit_price', 'price_with_tax', 'collection']

    # Custom field that is not in the model but will be created in the JSON
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
